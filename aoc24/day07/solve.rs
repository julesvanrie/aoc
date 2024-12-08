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

        let options_one: Vec<i64> = calc_one(numbers[0], &numbers, 1);
        let options_two: Vec<i64> = calc_two(numbers[0], &numbers, 1);

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

fn calc_one(base: i64, numbers: &[i64], index: usize) -> Vec<i64> {
    match numbers.len() - index {
        1 => vec![
            base + numbers[index],
            base * numbers[index]
        ],
        _ => [
            calc_one(base + numbers[index], &numbers, index+1),
            calc_one(base * numbers[index], &numbers, index+1)
        ].concat()
    }
}

fn calc_two(base: i64, numbers: &[i64], index: usize) -> Vec<i64> {
    match numbers.len() - index{
        1 => vec![
            base + numbers[index],
            base * numbers[index],
            base * (10i64.pow(numbers[index].ilog10()+1)) + numbers[index]
        ],
        _ => [
            calc_two(base + numbers[index], &numbers, index+1),
            calc_two(base * numbers[index], &numbers, index+1),
            calc_two(base * (10i64.pow(numbers[index].ilog10()+1)) + numbers[index], &numbers, index+1)
        ].concat()
    }
}
