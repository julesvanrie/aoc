use std::env;
use std::fs;
use std::error::Error;
extern crate regex;
use regex::Regex;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input();
    solve(&input);
    Ok(())
}

fn read_input() -> String {
    let args: Vec<String> = env::args().collect();
    let file_name = format!("{}.txt", &args[1]);
    fs::read_to_string(file_name)
        .unwrap()
}


fn solve(input: &String) {
    let mut result_one = 0i32;
    let mut result_two = 0i32;

    let re_big = Regex::new(r"(mul\((\d+),(\d+)\)|do\(\)|don't\(\))").unwrap();
    // let re_ops = Regex::new(r"(\d+)").unwrap();

    let mut enabled = true;
    for instruction in re_big.captures_iter(&input) {
        match &instruction[0][..3] {
            "mul" => {
                let left = &instruction[2].parse::<i32>().unwrap();
                let right = &instruction[3].parse::<i32>().unwrap();
                let mul = left * right;
                result_one += mul;
                if enabled { result_two += mul };
            },
            "do(" => enabled = true,
            "don" => enabled = false,
            _ => println!("Aaaarghh")
        }
    }

    println!("The answer for part 1 is: {}", result_one);
    println!("The answer for part 2 is: {}", result_two);
}
