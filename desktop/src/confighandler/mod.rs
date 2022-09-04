use std::{fs::File, io::Read};
use try_catch::catch;
use serde_json::from_str;
use defaultconfigs::Mainconfig;

use crate::defaultconfigs::{self, CONFIG_PATH};

extern crate serde;
extern crate serde_json;

pub(crate) fn init() {
    catch! {
        try {
            load()
        } catch _error {
            create()
        }
    }
}

fn load() {
    // Load the config file
    let mut file = File::open(CONFIG_PATH).unwrap();
    let mut contents = String::new();
    file.read_to_string(&mut contents).unwrap();
    let config: Mainconfig = from_str(&contents).unwrap();
    println!("{:?}", config);
}

fn create() {
    // Create the config file

}

fn save() {
    // Save the config file

}