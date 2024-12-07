use std::env;
use std::fs;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input();
    solve(input);
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

fn solve(input: Vec<String>) {
    let mut result_one = 0;
    let mut result_two = 0;

    for line in input {
        let (test, numbers): (i64, Vec<i64>)
            = line.split_once(": ")
                  .map(|(t, n)|
                       (t.parse::<i64>().unwrap(),
                        n.split(' ').map(|i| i.parse::<i64>().unwrap()).collect()))
                  .unwrap();

        let options_one: Vec<i64> = calc_one(&numbers);
        let options_two: Vec<i64> = calc_two(&numbers);

        if options_one.contains(&test) {
            result_one += &test;
        }
        if options_two.contains(&test) {
            result_two += &test;
        }
    }
    println!("The answer for part 1 is: {}", result_one);
    println!("The answer for part 2 is: {}", result_two);
}

fn calc_one(numbers: &Vec<i64>) -> Vec<i64> {
    match numbers.len() {
        2 => vec![
            numbers[0] + numbers[1],
            numbers[0] * numbers[1]
        ],
        _ => [
            calc_one(&[&[numbers[0] + numbers[1]], &numbers[2..]].concat()),
            calc_one(&[&[numbers[0] * numbers[1]], &numbers[2..]].concat())
        ].concat()
    }
}

fn calc_two(numbers: &Vec<i64>) -> Vec<i64> {
    match numbers.len() {
        2 => vec![
            numbers[0] + numbers[1],
            numbers[0] * numbers[1],
            numbers[0] * (10i64.pow(numbers[1].ilog10()+1)) + numbers[1]
        ],
        _ => [
            calc_two(&[&[numbers[0] + numbers[1]], &numbers[2..]].concat()),
            calc_two(&[&[numbers[0] * numbers[1]], &numbers[2..]].concat()),
            calc_two(&[&[numbers[0] * (10i64.pow(numbers[1].ilog10()+1)) + numbers[1]], &numbers[2..]].concat())
        ].concat()
    }
}
