use std::path::{PathBuf};

use serde::{Serialize, Deserialize};
use dirs::config_dir;

const SYSTEM_CONFIG_PATH: Option<PathBuf> = config_dir();
const RELATIVE_CONFIG_PATH: &str = "/pi-server-rack/config.json";

pub(crate) const VERSION: &str = env!("CARGO_PKG_VERSION");

pub(crate) const CONFIG_PATH: PathBuf=  SYSTEM_CONFIG_PATH.push(RELATIVE_CONFIG_PATH); //TODO: not die from fucking rust paths

#[derive(Serialize, Deserialize, Debug)]
pub(crate) struct Mainconfig {
    lang : String,
    configpath : String,
    customwindowframe : bool,

}