use image::DynamicImage;

pub fn has_alpha(img: &DynamicImage) -> bool {
    img.color().has_alpha()
}
