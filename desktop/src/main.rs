//import ui
mod ui;
pub(crate) mod confighandler;
pub(crate) mod defaultconfigs;

use defaultconfigs::VERSION;

use log::{info};

fn main() {
    info!(target: "[THREAD-MAIN]", "Welcome to PI-Server-Rack v{} !", VERSION);
    //initialize config
    confighandler::init();


    //initialiaze ui
    ui::mainloop();
}