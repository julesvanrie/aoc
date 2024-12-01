use std::env;
use std::io::{self, BufRead};
use std::fs::File;
use std::error::Error;
use std::str::FromStr;

fn main() -> Result<(), Box<dyn Error>> {
    let mut input = read_input()?;
    solve(&mut input);
    Ok(())
}

fn read_input() -> io::Result<io::Lines<io::BufReader<File>>> {
    let args: Vec<String> = env::args().collect();
    let file_name = format!("{}.txt", &args[1]);
    let file = File::open(file_name)?;
    Ok(io::BufReader::new(file).lines())
}

fn solve(input: &mut io::Lines<io::BufReader<File>>) {
    let mut answer_one = 0;
    let mut answer_two = 0;

    let mut lefties = vec![];
    let mut righties = vec![];

    input
        .map(|line| line.unwrap().split("   ")
                        .map(|item| i32::from_str(item).unwrap())
                        .collect()
        )
        .for_each(|couple: Vec<i32>| {
            lefties.push(couple[0]);
            righties.push(couple[1]);
        });

    lefties.sort();
    righties.sort();

    for (left, right) in std::iter::zip(&lefties, &righties) {
        answer_one += (left - right).abs();
        answer_two += left *
                      righties.iter()
                              .filter(|right| *right == left)
                              .count() as i32;
    }

    println!("The answer for part 1 is: {}", answer_one);
    println!("The answer for part 2 is: {}", answer_two);
}
