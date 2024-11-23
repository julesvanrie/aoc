use std::env;
use std::fs;
use std::error::Error;
// use std::collections::HashMap;
extern crate regex;
use regex::Regex;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input();

    solve_one(&input)?;
    solve_two(&input)?;

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

fn solve_one(input: &Vec<String>) -> Result<(), Box<dyn Error>> {
    let mut answer_one = 0;

    let re_quote_or_backslash = Regex::new(
        r###"(?m)(\\["\\])"###
    ).unwrap();
    let re_escaped = Regex::new(
        r###"(?m)(\\x[a-f0-9]{2})"###
    ).unwrap();


    for line in input {
        answer_one += 2;
        answer_one += re_quote_or_backslash.find_iter(&line).count();
        answer_one += re_escaped.find_iter(&line).count() * 3;
    }

    println!("The answer for part 1 is: {}", answer_one);
    Ok(())
}


fn solve_two(input: &Vec<String>) -> Result<(), Box<dyn Error>> {
    let mut answer_two = 0;

    let re_quote = Regex::new(
        r###"(?m)(\\|")"###
    ).unwrap();

    for line in input {
        answer_two += 2;
        answer_two += re_quote.find_iter(&line).count();
    }

    println!("The answer for part 2 is: {}", answer_two);
    Ok(())
}
