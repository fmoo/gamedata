/**
 * Difficulties
 */
enum Rating {
  WARMUP = 0,
  SIMPLE = 1,
  MODERATE = 2,
  TOUGH = 3,
  LEGIT = 4,
  HARDCORE = 5,
  OFF_THE_HOOK = 6,
}

/**
 * Formats
 */
const string DLC = 'Downloadable';
const string DC1 = 'On Disc - DC 1';
const string DC2 = 'On Disc - DC 2';
const string DC3 = 'On Disc - DC 3';


struct DanceCentralSourceSong {
  15: string title,
  1: string artist,

  /**
   * URL Path under http://www.dancecentral.com
   */
  2: string artwork,

  3: string choreographer,

  /**
   * Unused
   */
  4: string content,
  5: string credit,
  6: string decade,

  /**
   * English representation of difficulty corresponding to `rating`
   *
   * NOTE: Sometimes this is unpopulated for some reason
   */
  7: string difficulty,

  8: string format,
  9: string genre,

  /**
   * Price (for DLC only)
   *
   * NOTE: This is sometimes unpopulated, is occasionally wrong, and is
   * currently in points instead of local currency
   */
  10: string price,

  /**
   * Numerical difficulty corresponding to `difficulty`.
   */
  11: i16 rating,
  12: string release,
  13: string shortname,
  14: string sortdate,
  16: string url,

  /**
   * URL to xbox marketplace to buy online (DLC only)
   */
  17: string xbox,
}

typedef list<DanceCentralSourceSong> DanceCentralSourceSongList
