use std::env;
use std::fs;
use std::error::Error;
use std::str::FromStr;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input();

    solve_one(&input);
    solve_two(&input);

    Ok(())
}

fn read_input() -> Vec<String> {
    let args: Vec<String> = env::args().collect();
    let file_name = format!("{}.txt", &args[1]);
    fs::read_to_string(file_name)
        .unwrap()
        .lines()
        .map(String::from)
        .collect()
}

fn solve_one(input: &Vec<String>) {
    let mut counter = 0;

    for line in input {
        let mut nice = false;
        let mut vowels = 0;
        for c in line.chars() {
            if "aeiou".contains(c) {
                vowels += 1;
                if vowels == 3 { break } // Could be nice
            }
        }
        if vowels < 3 { continue } // Definitely not nice
        for c in "abcdefghijklmnopqrstuvwxyz".chars() {
            if line.contains(&format!("{}{}", c, c)) {
                nice = true;
            }
        }
        for combo in ["ab", "cd", "pq", "xy"] {
            if line.contains(combo) {
                nice = false;
            }
        }
        if nice { counter += 1 }
    }

    println!("The answer for part 1 is: {}", counter);
}

fn solve_two(input: &Vec<String>) {
    let mut counter = 0;

    for line in input {
        let mut nice = false;
        let mut condition_one = false;
        for i in 0..(line.len()-3) {
            if line[i+2..].contains(&line[i..i+2]) {
                condition_one = true;
                break;
            }
        }
        if !condition_one { continue } // Definitely not nice
        for i in 0..(line.len()-2) {
            if line[i+2..i+3] == line[i..i+1] {
                nice = true;
                break;
            }
        }
        if nice { counter += 1 }
    }

    println!("The answer for part 2 is: {}", counter);
}
