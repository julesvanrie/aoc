use std::env;
use std::fs;
use std::error::Error;
extern crate itertools;
use itertools::Itertools;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input();
    solve_one(&input);
    solve_two(&input);
    Ok(())
}

fn read_input() -> Vec<Vec<char>> {
    let args: Vec<String> = env::args().collect();
    let file_name = format!("{}.txt", &args[1]);
    fs::read_to_string(file_name)
        .unwrap()
        .lines()
        .map(String::from)
        .map(|line| line.chars().collect())
        .collect()
}

fn solve_one(input: &Vec<Vec<char>>) {
    let mut result = 0;
    let h = input.len();
    let w = input[0].len();

    for (y, x) in (0..h).cartesian_product(0..w) {
        if x < w-3 {
            // Horizontal
            match String::from_iter(&input[y][x..x+4]).as_str() {
                "XMAS" | "SAMX" => result += 1,
                _ => ()
            }
            // Diagonal like \
            if y < h-3 {
                match (0..4).map(|i| input[y+i][x+i]).collect::<String>().as_str() {
                    "XMAS" | "SAMX" => result += 1,
                    _ => ()
                }
            }
        }
        if y < h-3 {
            // Vertical
            match input[y..y+4].iter().map(|line| line[x]).collect::<String>().as_str() {
                "XMAS" | "SAMX" => result += 1,
                _ => ()
            }
            // Diagonal like /
            if x >= 3 {
                match (0..4).map(|i| input[y+i][x-i]).collect::<String>().as_str() {
                    "XMAS" | "SAMX" => result += 1,
                    _ => ()
                }
            }
        }
    }
    println!("The answer for part 1 is: {}", result);
}

fn solve_two(input: &Vec<Vec<char>>) {
    let mut result = 0;
    let h = input.len();
    let w = input[0].len();

    for (y, x) in (1..h-1).cartesian_product(1..w-1) {
        let letters: String = [
            input[y-1][x-1],
            input[y-1][x+1],
            input[y][x],
            input[y+1][x-1],
            input[y+1][x+1]
        ].into_iter().collect();
        let valids = vec!["MSAMS", "SMASM", "MMASS", "SSAMM"];
        if valids.contains(&letters.as_str()) {
            result += 1;
        }
    }
    println!("The answer for part 2 is: {}", result);
}
