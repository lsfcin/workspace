// caveman — shared configuration resolver, and the façade the hooks import
//
// Resolution order for the default mode:
//   1. CAVEMAN_DEFAULT_MODE environment variable
//   2. Config file `defaultMode` field:
//      - $XDG_CONFIG_HOME/caveman/config.json (any platform, if set)
//      - ~/.config/caveman/config.json (macOS / Linux fallback)
//      - %APPDATA%\caveman\config.json (Windows fallback)
//   3. 'full'
//
// Flag-file I/O lives in flagfile.js (over safepath.js) and is re-exported here,
// so every hook keeps importing exactly one module: `require('./config')`.

const fs = require('fs');
const path = require('path');
const os = require('os');
const flagfile = require('./flagfile');

const VALID_MODES = [
  'off', 'lite', 'full', 'ultra',
  'wenyan-lite', 'wenyan', 'wenyan-full', 'wenyan-ultra',
  'commit', 'review', 'compress'
];

function getConfigDir() {
  if (process.env.XDG_CONFIG_HOME) {
    return path.join(process.env.XDG_CONFIG_HOME, 'caveman');
  }
  if (process.platform === 'win32') {
    return path.join(
      process.env.APPDATA || path.join(os.homedir(), 'AppData', 'Roaming'),
      'caveman'
    );
  }
  return path.join(os.homedir(), '.config', 'caveman');
}

function getConfigPath() {
  return path.join(getConfigDir(), 'config.json');
}

function getDefaultMode() {
  // 1. Environment variable (highest priority)
  const envMode = process.env.CAVEMAN_DEFAULT_MODE;
  if (envMode && VALID_MODES.includes(envMode.toLowerCase())) {
    return envMode.toLowerCase();
  }

  // 2. Config file
  try {
    const config = JSON.parse(fs.readFileSync(getConfigPath(), 'utf8'));
    if (config.defaultMode && VALID_MODES.includes(config.defaultMode.toLowerCase())) {
      return config.defaultMode.toLowerCase();
    }
  } catch (e) {
    // Config file doesn't exist or is invalid — fall through
  }

  // 3. Default
  return 'full';
}

// The mode whitelist is policy and lives here, so flagfile.js takes it as an
// argument rather than importing back the other way.
function readFlag(flagPath) {
  return flagfile.readFlag(flagPath, VALID_MODES);
}

module.exports = {
  VALID_MODES,
  getConfigDir,
  getConfigPath,
  getDefaultMode,
  readFlag,
  safeWriteFlag: flagfile.safeWriteFlag,
  appendFlag: flagfile.appendFlag,
  readHistory: flagfile.readHistory
};
