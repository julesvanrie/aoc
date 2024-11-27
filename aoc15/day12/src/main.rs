use std::env;
use std::fs;
use std::error::Error;
extern crate regex;
use regex::Regex;
use serde_json;
use serde_json::Value::{Object, Array, Number};

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input();

    solve_one(&input)?;
    solve_two(&input)?;

    Ok(())
}

fn read_input() -> String {
    let args: Vec<String> = env::args().collect();
    let file_name = format!("{}.txt", &args[1]);
    fs::read_to_string(file_name)
        .unwrap()
}

fn solve_one(input: &String) -> Result<(), Box<dyn Error>> {
    let re = Regex::new(r###"(?m)(-?\d+)"###).unwrap();

    let mut results = vec![];
    for (_, [nb]) in re.captures_iter(input).map(|c| c.extract()) {
        results.push(nb.parse::<i32>()?);
    }

    println!("The answer for part 1 is: {}", results.into_iter().sum::<i32>());
    Ok(())
}

fn solve_two(input: &String) -> Result<(), Box<dyn Error>> {
    let structure: serde_json::Value =
        serde_json::from_str(input).unwrap();
    println!("The answer for part 2 is: {}", treatment(&structure));
    Ok(())
}

fn treatment(structure: &serde_json::Value) -> i64 {
      match &structure {
        Object(item) => match item.values().any(|i| i == "red") {
            true     => 0,
            false    => item.into_iter().map(|(_k, v)| treatment(v)).sum()
        },
        Array(item)  => item.into_iter().map(|i| treatment(i)).sum(),
        Number(item) => item.as_i64().unwrap(),
        _ => 0
    }
}
