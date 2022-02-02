use eframe::{egui::{self, TextureId}, epi};
use std::{sync::mpsc::{sync_channel, channel, Receiver, Sender, TryRecvError}, time::Duration, fmt::Result};
use rayon::prelude::*;
#[derive(serde::Deserialize, serde::Serialize)]
#[serde(default)] // if we add new fields, give them default values when deserializing old state
pub struct CaptureSettings {
    /// minimum time between captures in seconds
    min_frame_time: f32,
    #[serde(skip)]
    height: usize,
    #[serde(skip)]
    width: usize,
}
impl Default for CaptureSettings {
    fn default() -> Self {
        Self {
            min_frame_time: 1.0/24.0,
            height: 1080,
            width: 1920,
        }
    }
}

enum CaptureThreadMessage {
    Resume,
    Pause,
    Stop,
    UpdateFrameTime(Duration),
}

/// We derive Deserialize/Serialize so we can persist app state on shutdown.
#[derive(serde::Deserialize, serde::Serialize)]
#[serde(default)] // if we add new fields, give them default values when deserializing old state
pub struct AssistApp {
    capture_settings: CaptureSettings,
    #[serde(skip)]
    reciver: Option<Receiver<Vec<u8>>>,
    #[serde(skip)]
    sender: Option<Sender<CaptureThreadMessage>>,
    #[serde(skip)]
    screen_texture: Option<TextureId>,
}
impl Default for AssistApp {
    fn default() -> Self {
        Self {
            capture_settings: 
                CaptureSettings {
                    min_frame_time: 1.0/24.0,
                    height: 2160,
                    width: 3840,
                },
            reciver: None,
            sender: None,
            screen_texture: None,
        }
    }
}
impl epi::App for AssistApp {
    fn name(&self) -> &str {
        "AssistApp"
    }

    /// Called once before the first frame.
    fn setup(
        &mut self,
        _ctx: &egui::CtxRef,
        _frame: &epi::Frame,
        _storage: Option<&dyn epi::Storage>,
    ) {
        // Load previous app state (if any).
        if let Some(storage) = _storage {
            *self = epi::get_value(storage, epi::APP_KEY).unwrap_or_default()
        }

        println!("creating capture device");
        let (sender, reciver, width, height) = AssistApp::start_capture_thread();
        self.sender = Some(sender);
        self.reciver = Some(reciver);
        self.capture_settings.width = width;
        self.capture_settings.height = height;
        let new_frame = eframe::epi::Image::from_rgba_unmultiplied(
            [self.capture_settings.width, self.capture_settings.height],
            &self.reciver.as_mut().unwrap().recv().unwrap(),
        );
        self.screen_texture = Some(_frame.alloc_texture(new_frame));
    }

    /// Called by the frame work to save state before shutdown.
    fn save(&mut self, storage: &mut dyn epi::Storage) {
        epi::set_value(storage, epi::APP_KEY, self);
    }

    /// Called each time th UI needs repainting, which may be many times per second.
    /// Put your widgets into a `SidePanel`, `TopPanel`, `CentralPanel`, `Window` or `Area`.
    fn update(&mut self, ctx: &egui::CtxRef, frame: &epi::Frame) {
        // let Self { capture_settings, capturer, latest_frame } = self;

        egui::TopBottomPanel::top("top_panel").show(ctx, |ui| {
            // The top panel is often a good place for a menu bar:
            egui::menu::bar(ui, |ui| {
                ui.menu_button("File", |ui| {
                    if ui.button("Quit").clicked() {
                        frame.quit();
                    }
                });
                ui.menu_button("Screen Capture", |ui| {
                    if ui.button("Toggle Show frame").clicked() {
                        if self.screen_texture.is_none() {
                            self.show_new_frame(frame);
                        } else {
                            self.screen_texture = None;
                        }
                        ui.close_menu();
                    }
                    if self.screen_texture.is_some() && ui.button("Refresh frame").clicked() {
                        self.show_new_frame(frame);
                    }
                });
                egui::warn_if_debug_build(ui);
            });
        });

        if self.screen_texture.is_some() {
            egui::Window::new("Preview")
            .title_bar(false)
            .resizable(true)
            .show(ctx, |inner_ui| {
                inner_ui.image(self.screen_texture.unwrap(), [] );
            });
        }
        // try get new frame
        // if let Ok(new) = self.reciver.as_mut().unwrap().try_recv() {
        //     println!("got new frame");
        //     // free previous frame
        //     // if self.screen_texture.is_some() {
        //     //     frame.free_texture(self.screen_texture.unwrap());
        //     // }
        //     // alloc new frame
        //     let new_frame = eframe::epi::Image::from_rgba_unmultiplied(
        //         [self.capture_settings.width, self.capture_settings.height],
        //         &new
        //     );
        //     self.screen_texture = Some(frame.alloc_texture(new_frame));
        // }

        // egui::SidePanel::left("side_panel").show(ctx, |ui| {

        // });

        egui::CentralPanel::default().show(ctx, |ui| {
            // The central panel the region left after adding TopPanel's and SidePanel's
            if self.screen_texture.is_some() {
                ui.image(self.screen_texture.unwrap(), [self.capture_settings.width as f32 / 4.0, self.capture_settings.height as f32/ 4.0] );
            }
        });
    }

    // fn on_exit(&mut self) {
    // }
}
impl AssistApp {
    fn show_new_frame(&mut self, frame: &epi::Frame) {
        let new = self.reciver.as_mut().unwrap().recv().unwrap();
        println!("got new frame");
        // free previous frame
        if self.screen_texture.is_some() {
            frame.free_texture(self.screen_texture.unwrap());
        }
        // alloc new frame
        let new_frame = eframe::epi::Image::from_rgba_unmultiplied(
            [self.capture_settings.width, self.capture_settings.height],
            &new
        );
        self.screen_texture = Some(frame.alloc_texture(new_frame));
        
    }
    /// Returns (sender into capture thread, receiver from capture thread, frame width, frame height)
    fn start_capture_thread() -> (Sender<CaptureThreadMessage>, Receiver<Vec<u8>>, usize, usize) {
        // start capturing loop on another thread
        let (sender, reciver) = sync_channel::<Vec<u8>>(0);
        let (sender2, reciver2) = channel::<CaptureThreadMessage>();
        // let temp_disp = scrap::Display::primary().unwrap();
        // let width = temp_disp.width();
        // let height = temp_disp.height();
        let width = 3840;
        let height = 2160;
        std::thread::Builder::new().name("screen_capture_thread".into()).spawn(move || {
            let sender = sender;
            let reciver = reciver2;
            let mut capturer = scrap::Capturer::new(scrap::Display::primary().unwrap()).unwrap();
            let mut previous_time = std::time::Instant::now();

            // spinlock until we get first frame
            const CAPTURE_TIMEOUT: std::time::Duration = std::time::Duration::from_secs(5);
            loop {
                if let Ok(_) = capturer.frame() {
                    break;
                }
                if previous_time.elapsed() > CAPTURE_TIMEOUT {
                    panic!("failed to get first frame from capturer within {} seconds", CAPTURE_TIMEOUT.as_secs_f32());
                }
                std::thread::sleep(std::time::Duration::from_millis(100));
            };
            let mut paused = false;
            let mut min_frame_time = Duration::from_secs_f32(1.0 / 60.0);
            let mut message;
            loop {
                if paused {
                    match reciver.recv() {
                        Ok(m) => {message = Ok(m);},
                        Err(_) => break,
                    }
                } else {
                    message = reciver.try_recv();
                }
                match message {
                    Ok(CaptureThreadMessage::Stop) => {
                        break;
                    }
                    Ok(CaptureThreadMessage::UpdateFrameTime(new_time)) => {
                        min_frame_time = new_time;
                    }
                    Ok(CaptureThreadMessage::Resume) => {paused = false;},
                    Ok(CaptureThreadMessage::Pause) => {paused = true;},
                    Err(e) => {
                        match e {
                            TryRecvError::Disconnected => {
                                break;
                            }
                            TryRecvError::Empty => {}
                        }
                    }
                }
                let cap = capturer.frame();
                if let Ok(inside) = cap {
                    let mut inside = inside.to_owned();
                    inside.par_chunks_exact_mut(4).for_each(|chunk| {
                        let b = chunk[0];
                        let r = chunk[2];
                        chunk[0] = r;
                        chunk[2] = b;
                        chunk[3] = 255;
                    });
                    if sender.send(inside).is_err() {
                        break;
                    }
                }
                if previous_time.elapsed() < min_frame_time {
                    std::thread::sleep(min_frame_time - previous_time.elapsed());
                } 
                previous_time = std::time::Instant::now();
            }
        }).unwrap();
        (sender2, reciver, width, height)
    }
}
