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

    let re_signal = Regex::new(r"^\d+$").unwrap();
    let re_wire = Regex::new(r"^[a-z]+$").unwrap();
    let re_not = Regex::new(r"^NOT ([a-z]+)$").unwrap();
    let re_num_and = Regex::new(r"^(\d+) AND ([a-z]+)$").unwrap();
    let re_and = Regex::new(r"^([a-z]+) AND ([a-z]+)$").unwrap();
    let re_or  = Regex::new(r"^([a-z]+) OR ([a-z]+)$").unwrap();
    let re_lsh = Regex::new(r"^([a-z]+) LSHIFT (\d+)$").unwrap();
    let re_rsh = Regex::new(r"^([a-z]+) RSHIFT (\d+)$").unwrap();

    let mut previous_len = 0;
    loop {
        for (_, [left, right])
            in re.captures_iter(input)
                        .map(|c| c.extract()) {

                            // Signal
            if re_signal.captures(left).is_some() {
                wires.insert(right, left.parse().unwrap());
            }
            // Wire
            if re_wire.captures(left).is_some() {
                if let Some(one) = wires.get(left) {
                    wires.insert(right, *one);
                }
            }
            // NOT
            if let Some(wire) = re_not.captures(left) {
                if let Some(one) = wires.get(&wire[1]) {
                    wires.insert(right, !one);
                };
            }
            // number AND
            if let Some(wire) = re_num_and.captures(left) {
                let one: u16 = wire[1].parse().unwrap();
                if let Some(two) = wires.get(&wire[2]) {
                    wires.insert(right, one & two);
                }
            }
            // AND
            if let Some(wire) = re_and.captures(left) {
                if let Some(one) = wires.get(&wire[1]) {
                    if let Some(two) = wires.get(&wire[2]) {
                        wires.insert(right, one & two);
                    }
                }
            }
            // OR
            if let Some(wire) = re_or.captures(left) {
                if let Some(one) = wires.get(&wire[1]) {
                    if let Some(two) = wires.get(&wire[2]) {
                        wires.insert(right, one | two);
                    }
                }
            }
            // LSHIFT
            if let Some(wire) = re_lsh.captures(left) {
                if let Some(one) = wires.get(&wire[1]) {
                      wires.insert(right, one << (&wire[2]).parse::<u16>().unwrap());
                };
            }
            // RSHIFT
            if let Some(wire) = re_rsh.captures(left) {
                if let Some(one) = wires.get(&wire[1]) {
                    wires.insert(right, one >> (&wire[2]).parse::<u16>().unwrap());
                };
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
