use std::{
    fs::{File, remove_dir_all, create_dir},
    io::Write,
};
pub fn main() {
    // reset asset build folder 
    remove_dir_all("assets/build").ok();
    create_dir("assets/build").unwrap();

    convert_icon_to_rgba8()
}

fn convert_icon_to_rgba8() {
    // load icon data
    let image = image::open("assets/icon.png").unwrap();
    let rgba8 = image.to_rgba8();
    let new_file_path = "assets/build/icon.rgba8";
    let mut file = File::create(&new_file_path).unwrap();
    file.write_all(&rgba8.as_raw()).unwrap();
    println!("cargo:rerun-if-changed=assets/icon.png");
    println!("cargo:rerun-if-changed={:?}", &new_file_path);
}