use std::env;
use std::fs;
use std::error::Error;
use std::collections::HashMap;
extern crate regex;
use regex::Regex;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input();

    solve_one(&input)?;
    println!("For part two: in the input file find the line that sets b and change its input to a.");
    Ok(())
}

fn read_input() -> String {
    let args: Vec<String> = env::args().collect();
    let file_name = format!("{}.txt", &args[1]);
    fs::read_to_string(file_name)
        .unwrap()
}

fn solve_one(input: &str) -> Result<(), Box<dyn Error>> {

    let mut wires: HashMap<&str, u16> = HashMap::new();

    let re = Regex::new(
        r"(?m)^([\w\s]+) -> ([a-z]+)$"
    ).unwrap();

    let re_signal = Regex::new(r"^\d+|[a-z]+$").unwrap();
    let re_not = Regex::new(r"^NOT ([a-z]+)$").unwrap();
    let re_binary = Regex::new(r"^(\d+|[a-z]+) ([A-Z]+) (\d+|[a-z]+)$").unwrap();

    let mut previous_len = 0;
    loop {
        for (_, [left, right])
            in re.captures_iter(input).map(|c| c.extract()) {

            // Signal
            if re_signal.captures(left).is_some() {
                if let Some(left) = match left.parse::<u16>() {
                    Ok(v) => Some(v),
                    Err(_e) => wires.get(&left).copied()
                } {
                    wires.insert(right, left);
                }
            }
            // NOT
            if let Some(wire) = re_not.captures(left) {
                if let Some(one) = wires.get(&wire[1]) {
                    wires.insert(right, !one);
                };
            }
            // AND
            if let Some(wire) = re_binary.captures(left) {
                if let Some(one) = match wire[1].parse::<u16>() {
                    Ok(v) => Some(v),
                    Err(_e) => wires.get(&wire[1]).copied()
                } {
                    if let Some(two) = match wire[3].parse::<u16>() {
                        Ok(v) => Some(v),
                        Err(_e) => wires.get(&wire[3]).copied()
                    } {
                        wires.insert(
                            right,
                            match &wire[2] {
                                "AND" => one & two,
                                "OR" => one | two,
                                "LSHIFT" => one << two,
                                "RSHIFT" => one >> two,
                                _ => 0
                            });
                    }
                }
            }
        }

        if wires.len() > previous_len {
            previous_len = wires.len();
        } else {
            break
        };

    }

    println!("The answer for part 1 is: {}", wires.get("a").unwrap());
    Ok(())
}
