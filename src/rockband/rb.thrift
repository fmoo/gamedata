

enum Difficulty {
  NO_PART = -1,  // Negative values are disallowed for enums? :(
  ZERO = 0,
  ONE = 1,
  TWO = 2,
  THREE = 3,
  FOUR = 4,
  FIVE = 5,
  FIVE_SKULLS = 6,
}

/**
 * Valid `source` values
 */
const string SOURCE_ROCK_BAND_1 = "RB1";
const string SOURCE_ROCK_BAND_2 = "RB2";
const string SOURCE_ROCK_BAND_3 = "RB3";
const string SOURCE_DLC = "DLC";
const string SOURCE_ROCK_BAND_NETWORK = "RBN";
const string SOURCE_LEGO_ROCK_BACK = "LEGO";
const string SOURCE_GREEN_DAY_ROCK_BAND = "GDRB";


/**
 * A thrift structure that maps to the json structure fetched from rockband.com
 */
struct RockBandSourceSong {
  1: string artist,
  2: string artist_tr,
  3: bool cover,
  4: string decade,
  5: Difficulty difficulty_band,
  6: Difficulty difficulty_bass,
  7: Difficulty difficulty_drums,
  8: Difficulty difficulty_guitar,
  9: Difficulty difficulty_keys,
  10: Difficulty difficulty_pro_bass,
  11: Difficulty difficulty_pro_drums,
  12: Difficulty difficulty_pro_guitar,
  13: Difficulty difficulty_pro_keys,
  14: Difficulty difficulty_vocals,
  15: string genre_symbol,

  /**
   * Some unique(?) numeric identifier.
   *
   * NOTE: There seem to be duplicates
   */
  16: string id,
  17: bool is_rb3_only,
  18: string name,
  19: string name_tr,
  20: string rating,  // (popularity?)

  /**
   * Actual unique identifier?  Seems to contain `id`
   */
  21: string shortname,

  22: string source,

  23: string starts_with,
  24: bool upgrades_available,
  25: string vocal_parts,
  26: string year_released,
}

typedef list<RockBandSourceSong> RockBandSourceSongList

// Some additional fields that would be nice to have and are accessible via
// other pages on the site (e.g., /songs/{shortname})
//
// Album
// Label
// DLC Release Date
// Rating (e.g., Family Friendly)
// Platform compatibility
// Track Author
// DLC Pack Info
// Purchase Links (e.g., to microsoft.com or psn websites)
