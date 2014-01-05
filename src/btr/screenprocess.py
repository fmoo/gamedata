from argparse import ArgumentParser
import os.path
import re
import sys
import pygame.image
from pygame.rect import Rect
from UserList import UserList
from pygame.surface import Surface
from pygame.color import Color
from collections import defaultdict
from operator import itemgetter


TILE_WIDTH = TILE_HEIGHT = 8
VIEWPORT_XOFFS = 32
VIEWPORT_YOFFS = 35
VIEWPORT_TILE_ROWS = 20
VIEWPORT_TILE_COLS = 40
VIEWPORT_RECT = Rect(VIEWPORT_XOFFS,VIEWPORT_YOFFS,
        TILE_WIDTH * VIEWPORT_TILE_COLS,
        TILE_HEIGHT * VIEWPORT_TILE_ROWS)


class Images(UserList):
    PREFIX = 'image'

    @classmethod
    def from_dir(cls, path):
        tiles = cls()
        for f in os.listdir(path):
            if re.match(cls.PREFIX + '\d+\.png', f) is not None:
                tiles.append(pygame.image.load(os.path.join(path, f)))
        return tiles

    def save_dir(self, path):
        for i, t in enumerate(self):
            pygame.image.save(t, os.path.join(path, '%s%d.png' %
                (self.PREFIX, i)))

    def find(self, item):
        for i, t in enumerate(self):
            if item.get_size() != t.get_size():
                continue

            skip = False
            w, h = item.get_size()
            for x in xrange(0, w):
                for y in xrange(0, h):
                    if item.get_at((x, y)) != t.get_at((x, y)):
                        skip = True
                        break
                if skip:
                    break

            if not skip:
                return i
        return -1

    def __contains__(self, item):
        return self.find(item) != -1

class Tiles(Images):
    PREFIX = 'tile'

class Sprites(Images):
    PREFIX = 'sprite'

def assert_same_sizes(surfaces):
    w, h = surfaces[0].get_size()
    for surface in surfaces[1:]:
        assert surface.get_size() == (w, h)
    return w, h


def normalize_images(images):
    assert len(images) >= 3
    print "Normalizing %d files..." % (len(images)),
    sys.stdout.flush()

    # Verify w/h same for all images
    w, h = assert_same_sizes(images)

    # TODO: Do this on a per-tile basis. Without means we
    # won't capture water correctly.
    newsurf = Surface((w, h))
    for x in xrange(0, w):
        for y in xrange(0, h):
            values = defaultdict(int)
            for i in images:
                k = tuple(i.get_at((x, y)))
                values[k] += 1
            value = sorted(values.items(), key=itemgetter(1))[-1]
            newsurf.set_at((x, y), Color(*value[0]))

    pygame.image.save(newsurf, 'normalized.png')
    print "Done!"

    return newsurf


def calculate_foreground(background, composite):
    print "Calculating foreground...",
    sys.stdout.flush()
    w, h = assert_same_sizes([background, composite])

    foreground = Surface((w, h), flags=pygame.SRCALPHA)
    for x in xrange(0, w):
        for y in xrange(0, h):
            baseline = tuple(background.get_at((x, y)))
            k = composite.get_at((x, y))
            if tuple(k) != baseline:
                foreground.set_at((x, y), k)
    pygame.image.save(foreground, 'foreground.png')
    print "done!"
    return foreground


def find_sprites(foreground, background):
    print "Finding sprites..."
    found_sprites = []
    found_rects = []
    w, h = foreground.get_size()
    for x in xrange(0, w):
        for y in xrange(0, h):
            skip = False
            for r in found_rects:
                if r.collidepoint((x, y)):
                    skip = True
                    break
            if skip:
                continue

            data = foreground.get_at((x, y))
            if any(data):
                print "Found pixel at", (x, y)
                print "Expanding rect...",
                sys.stdout.flush()
                found_rect = expand_sprite_rect(foreground, (x, y))
                if found_rect is None:
                    continue

                print "Expanded to rect: ", found_rect 
                found_rects.append(found_rect)

                # Save intermediate file
                sprite = foreground.subsurface(found_rect)

                # Make sure there are no *same color* pixels in the background
                sprite_color = data
                if check_texture_collision(background, foreground,
                                           found_rect, sprite_color):
                    print "Sprite on background of matching color.  Skipping"
                    continue

                pygame.image.save(sprite, "found_sprite.png")

                # TODO: If a found_rect overlaps another rect, remove the
                # smaller found_rect, append only the largest sprites.
                found_sprites.append(sprite)

    return found_sprites

def image_line_has_pixels(image, x0, x1, y0, y1):
    for x in xrange(x0, x1 + 1):
        for y in xrange(y0, y1 + 1):
            if any(image.get_at((x, y))):
                return True
    return False

def expand_sprite_rect(image, pos):
    any_change = True
    current_rect = Rect(pos[0], pos[1], 0, 0)
    try:
        while any_change:
            any_change = False
            # Expand and check each side.  If a side grows, set any_change to True

            # Right
            while image_line_has_pixels(image,
                    current_rect.x + current_rect.w + 1,
                    current_rect.x + current_rect.w + 1,
                    current_rect.y,
                    current_rect.y + current_rect.h):
                current_rect.w += 1
                any_change = True

            # Down
            while image_line_has_pixels(image,
                    current_rect.x,
                    current_rect.x + current_rect.w,
                    current_rect.y + current_rect.h + 1,
                    current_rect.y + current_rect.h + 1):
                current_rect.h += 1
                any_change = True

            # Up
            while image_line_has_pixels(image,
                    current_rect.x,
                    current_rect.x + current_rect.w,
                    current_rect.y - 1,
                    current_rect.y - 1):
                current_rect.h += 1
                current_rect.y -= 1
                any_change = True

            # Left
            while image_line_has_pixels(image,
                    current_rect.x - 1,
                    current_rect.x - 1,
                    current_rect.y,
                    current_rect.y + current_rect.h):
                current_rect.w += 1
                current_rect.x -= 1
                any_change = True

    except IndexError:
        print "Sprite on edge of surface.  Discarding."
        return None

    # wat?
    current_rect.w += 1
    current_rect.h += 1
    return current_rect

def subsurfaces(surfaces, rect):
    return [surface.subsurface(rect) for surface in surfaces]

def check_texture_collision(bg, fg, rect, sprite_color):
    for x in xrange(rect.x, rect.x + rect.w):
        for y in xrange(rect.y, rect.y + rect.h):
            fdata = fg.get_at((x, y))
            if any(fdata):
                continue
            bdata = bg.get_at((x, y))
            if bdata == sprite_color:
                return True
    return False

def main():
    ap = ArgumentParser()
    ap.add_argument('filename', nargs='+')
    ap.add_argument('--tiledir', default='./tiles')
    ap.add_argument('--spritedir', default='./sprites')

    ns = ap.parse_args()
    assert os.path.isdir(ns.tiledir)

    for filename in ns.filename:
        assert os.path.exists(filename)

    if len(ns.filename) == 1:
        filename = ns.filename[-1]
        img = pygame.image.load(filename)
        img, = subsurfaces([img], VIEWPORT_RECT) 
    else:
        all_images = subsurfaces([pygame.image.load(n) for n in ns.filename],
                                 VIEWPORT_RECT)
        img = normalize_images(all_images)

        # Initialize found sprites
        assert os.path.isdir(ns.spritedir)
        sprites = Sprites.from_dir(ns.spritedir)
        n_orig_sprites = len(sprites)
        print "Found %d sprites in '%s'" % (n_orig_sprites, ns.spritedir)

        # Look for sprites
        for i, other in enumerate(all_images):
            print "Looking for sprites in image %d" % (i + 1)
            fore = calculate_foreground(img, other)
            found_sprites = find_sprites(fore, img)
            for sprite in found_sprites:
                if sprite not in sprites:
                    sprites.append(sprite)

        n_new_sprites = len(sprites) - n_orig_sprites
        if n_new_sprites > 0:
            print "Found %d new sprites" % n_new_sprites
            if raw_input("Save sprites? [y/n]").lower().startswith('y'):
                sprites.save_dir(ns.spritedir)
                print "Saved!"

    tiles = Tiles.from_dir(ns.tiledir)
    n_orig_tiles = len(tiles)
    print "Found %d tiles in '%s'" % (n_orig_tiles, ns.tiledir)

    screen = {}
    w, h = img.get_size()
    for i, x in enumerate(xrange(0, w, TILE_WIDTH)):
        for j, y in enumerate(xrange(0, h, TILE_HEIGHT)):
            tile = img.subsurface(Rect(x, y, TILE_WIDTH, TILE_HEIGHT))
            tindex = tiles.find(tile)
            if tindex == -1:
                tiles.append(tile)
                #pygame.image.save(tile, "tile%d.png" % (len(tiles)))
            screen[(i, j)] = tindex

    n_new_tiles = len(tiles) - n_orig_tiles
    print "Found %d new tiles" % n_new_tiles

    if n_new_tiles > 0:
        if raw_input("Save tiles? [y/n]").lower().startswith('y'):
            tiles.save_dir(ns.tiledir)
            print "Saved!"

if __name__ == '__main__':
    main()
