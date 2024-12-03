use std::env;
use std::fs;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input();
    solve(&input);
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

fn solve(input: &Vec<String>) {
    let mut counter_one = 0;
    let mut counter_two = 0;
    for line in input {
        let numbers: Vec<i32> = line.split_whitespace()
                                    .map(|n| n.parse().unwrap())
                                    .collect();
        if is_safe(&numbers) {
            counter_one += 1;
        }
        if can_be_made_safe(&numbers) {
            counter_two += 1;
        }
    }

    println!("The answer for part 1 is: {}", counter_one);
    println!("The answer for part 2 is: {}", counter_two);
}

fn is_safe(numbers: &Vec<i32>) -> bool {
    let incr = numbers[numbers.len()-1] > numbers[0];
    for i in 0..numbers.len()-1 {
        if numbers[i+1] == numbers[i] {
            return false
        }
        if (numbers[i+1] - numbers[i]).abs() > 3 {
            return false
        }
        if (numbers[i+1] > numbers[i]) != incr {
            return false
        }
    }
    true
}

fn can_be_made_safe(numbers: &Vec<i32>) -> bool {
    for i in 0..numbers.len() {
        if is_safe(&[&numbers[..i], &numbers[i+1..]].concat()) {
            return true
        }
    }
    false
}
