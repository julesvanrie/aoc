#![allow(dead_code)]

use std::env;
use std::fs;
use std::error::Error;
use std::collections::HashMap;
use std::cmp::max;
extern crate regex;
use regex::Regex;

// For the slow implementation using HashMaps
#[derive(Hash, Eq, PartialEq, Debug)]
struct Coord { x: i32, y: i32 }
impl Coord {
    fn new(x: i32, y: i32) -> Coord {
        Coord { x: x, y: y }
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input();

    faster_one(&input)?;
    faster_two(&input)?;
    Ok(())
}

fn read_input() -> String {
    let args: Vec<String> = env::args().collect();
    let file_name = format!("{}.txt", &args[1]);
    fs::read_to_string(file_name)
        .unwrap()
}

// Slow implementation using HashMaps
// Did this because I assumed this was going to scale up some way
fn solve_one(input: &str) -> Result<(), Box<dyn Error>> {

    let mut lights: HashMap<Coord, bool> = HashMap::new();

    let re = Regex::new(
        r"(?m)^([a-z|\s]+) (\d+),(\d+) through (\d+),(\d+)$"
    ).unwrap();

    for (_, [action, xstart, ystart, xend, yend])
        in re.captures_iter(input)
                    .map(|c| c.extract()) {

        for x in xstart.parse::<i32>()?..(xend.parse::<i32>()?+1) {
        for y in ystart.parse::<i32>()?..(yend.parse::<i32>()?+1) {
            match action {
                "turn on"
                    => lights.insert(Coord::new(x, y), true),
                "turn off"
                    => lights.insert(Coord::new(x, y), false),
                "toggle"
                    => Some(*lights.entry(Coord::new(x, y))
                                    .and_modify(|state| *state = !*state)
                                    .or_insert(true)),
                _ => Some(false)
            };
        }
        }
    }

    let count_lights = lights.values().filter(|light| **light).count();
    println!("The answer for part 1 is: {}", count_lights);
    Ok(())
}

fn solve_two(input: &str) -> Result<(), Box<dyn Error>> {

    let mut lights: HashMap<Coord, i32> = HashMap::new();

    let re = Regex::new(
        r"(?m)^([a-z|\s]+) (\d+),(\d+) through (\d+),(\d+)$"
    ).unwrap();

    for (_, [action, xstart, ystart, xend, yend])
        in re.captures_iter(input)
                    .map(|c| c.extract()) {

        for x in xstart.parse::<i32>()?..(xend.parse::<i32>()?+1) {
        for y in ystart.parse::<i32>()?..(yend.parse::<i32>()?+1) {
            match action {
                "turn on"
                    => lights.entry(Coord::new(x, y))
                             .and_modify(|brightness| *brightness += 1)
                             .or_insert(1),
                "turn off"
                    => lights.entry(Coord::new(x, y))
                             .and_modify(|brightness| *brightness = max(0, *brightness - 1))
                             .or_insert(0),
                "toggle"
                    => lights.entry(Coord::new(x, y))
                             .and_modify(|brightness| *brightness += 2)
                             .or_insert(2),
                _ => &0
            };
        }
        }
    }

    let sum_lights = lights.values().sum::<i32>();
    println!("The answer for part 2 is: {}", sum_lights);
    Ok(())
}

// Fast implementation using a vector
fn faster_one(input: &str) -> Result<(), Box<dyn Error>> {
    // One dimensional vector: we'll multiple y with 1000 to wrap 2D in here
    let mut lights = [false; 1_000_000];

    let re = Regex::new(
        r"(?m)^([a-z|\s]+) (\d+),(\d+) through (\d+),(\d+)$"
    ).unwrap();

    for (_, [action, xstart, ystart, xend, yend])
        in re.captures_iter(input)
                    .map(|c| c.extract()) {

        for x in xstart.parse::<usize>()?..(xend.parse::<usize>()?+1) {
        for y in ystart.parse::<usize>()?..(yend.parse::<usize>()?+1) {
            match action {
                "turn on"
                    => lights[1000*y + x] = true,
                "turn off"
                    => lights[1000*y + x] = false,
                "toggle"
                    => lights[1000*y + x] = !lights[1000*y + x],
                _ => ()
            };
        }
        }
    }

    let count_lights = lights.into_iter().filter(|light| *light).count();
    println!("The answer for part 1 is: {}", count_lights);
    Ok(())
}

fn faster_two(input: &str) -> Result<(), Box<dyn Error>> {
    // One dimensional vector: we'll multiple y with 1000 to wrap 2D in here
    let mut lights = vec![0i32; 1_000_000];

    let re = Regex::new(
        r"(?m)^([a-z|\s]+) (\d+),(\d+) through (\d+),(\d+)$"
    ).unwrap();

    for (_, [action, xstart, ystart, xend, yend])
        in re.captures_iter(input)
                    .map(|c| c.extract()) {

        for x in xstart.parse::<usize>()?..(xend.parse::<usize>()?+1) {
        for y in ystart.parse::<usize>()?..(yend.parse::<usize>()?+1) {
            match action {
                "turn on"
                    => lights[1000*y + x] += 1,
                "turn off"
                    => lights[1000*y + x] = max(0, lights[1000*y + x] - 1),
                "toggle"
                    => lights[1000*y + x] += 2,
                _ => ()
            };
        }
        }
    }

    let sum_lights: i32 = lights.into_iter().sum::<i32>().into();
    println!("The answer for part 2 is: {}", sum_lights);
    Ok(())
}
