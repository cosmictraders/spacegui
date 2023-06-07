use iced::widget::{button, column, text};
use iced::{Alignment, Element, Length, Sandbox, Settings};

mod map;

pub fn main() -> iced::Result {
    MapDisplay::run(Settings {
        antialiasing: true,
        ..Settings::default()
    })
}

#[derive(Default)]
struct MapDisplay {
    map: map::State,
    curves: Vec<map::Curve>,
}

#[derive(Debug, Clone, Copy)]
enum Message {
    AddCurve(map::Curve),
    Reset,
}

impl Sandbox for MapDisplay {
    type Message = Message;

    fn new() -> Self {
        MapDisplay::default()
    }

    fn title(&self) -> String {
        String::from("Map v4")
    }

    fn update(&mut self, message: Message) {
        match message {
            Message::AddCurve(curve) => {
                self.curves.push(curve);
                self.map.request_redraw();
            }
            Message::Reset => {
                self.map = map::State::default();
                self.curves.clear();
            }
        }
    }

    fn view(&self) -> Element<Message> {
        column![
            self.map.view(&self.curves).map(Message::AddCurve),
            button("Reset").padding(8).on_press(Message::Reset),
        ]
        .padding(20)
        .spacing(20)
        .align_items(Alignment::Center)
        .into()
    }
}
