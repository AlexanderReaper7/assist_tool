
// When compiling natively:
#[cfg(not(target_arch = "wasm32"))]

fn main() {
    use eframe::epi::IconData;

    let app = assist_tool::AssistApp::default();
    let mut native_options = eframe::NativeOptions::default();

    // load icon data
    native_options.icon_data = Some(IconData {
        width: 512,
        height: 512,
        rgba: include_bytes!("../assets/build/icon.rgba8").to_vec(),
    });
    
    eframe::run_native(Box::new(app), native_options);
}
