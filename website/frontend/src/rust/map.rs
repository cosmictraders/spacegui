use iced::mouse;
use iced::widget::canvas::event::{self, Event};
use iced::widget::canvas::{
    self, Canvas, Cursor, Frame, Geometry, Path, Stroke,
};
use iced::{Element, Length, Point, Rectangle, Theme};

#[derive(Default)]
pub struct State {
    cache: canvas::Cache,
}

impl State {
    pub fn view<'a>(&'a self) -> Element<'a, Curve> {
        Canvas::new(Map {
            state: self,
            curves,
        })
        .width(Length::Fill)
        .height(Length::Fill)
        .into()
    }

    pub fn request_redraw(&mut self) {
        self.cache.clear()
    }
}

struct Map<'a> {
    curves: &'a [Curve],
}

impl<'a> canvas::Program for Map<'a> {

    fn update(
        &self,
        state: &mut Self::State,
        event: Event,
        bounds: Rectangle,
        cursor: Cursor,
    ) -> (event::Status, Option<Curve>) {
        let cursor_position =
            if let Some(position) = cursor.position_in(&bounds) {
                position
            } else {
                return (event::Status::Ignored, None);
            };

        match event {
            Event::Mouse(mouse_event) => {
                let message = match mouse_event {
                    mouse::Event::ButtonPressed(mouse::Button::Left) => {
                        match *state {
                            None => {
                                *state = Some(Pending::One {
                                    from: cursor_position,
                                });

                                None
                            }
                            Some(Pending::One { from }) => {
                                *state = Some(Pending::Two {
                                    from,
                                    to: cursor_position,
                                });

                                None
                            }
                            Some(Pending::Two { from, to }) => {
                                *state = None;

                                Some(Curve {
                                    from,
                                    to,
                                    control: cursor_position,
                                })
                            }
                        }
                    }
                    _ => None,
                };

                (event::Status::Captured, message)
            }
            _ => (event::Status::Ignored, None),
        }
    }

    fn draw(
        &self,
        state: &Self::State,
        _theme: &Theme,
        bounds: Rectangle,
        cursor: Cursor,
    ) -> Vec<Geometry> {
        let content =
            self.state.cache.draw(bounds.size(), |frame: &mut Frame| {
                Curve::draw_all(self.curves, frame);

                frame.stroke(
                    &Path::rectangle(Point::ORIGIN, frame.size()),
                    Stroke::default().with_width(2.0),
                );
            });

        if let Some(pending) = state {
            let pending_curve = pending.draw(bounds, cursor);

            vec![content, pending_curve]
        } else {
            vec![content]
        }
    }

    fn mouse_interaction(
        &self,
        _state: &Self::State,
        bounds: Rectangle,
        cursor: Cursor,
    ) -> mouse::Interaction {
        if cursor.is_over(&bounds) {
            mouse::Interaction::Text // TODO: Change
        } else {
            mouse::Interaction::default()
        }
    }
}
