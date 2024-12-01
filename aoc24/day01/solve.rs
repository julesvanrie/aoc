use std::env;
use std::fs;
use std::error::Error;
use std::str::FromStr;

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
    let mut answer_one = 0;
    let mut answer_two = 0;

    let mut lefties = vec![];
    let mut righties = vec![];

    // for line in input {
    //     let splitted: Vec<i32> = line.split("   ")
    //         .map(|num| i32::from_str(num).unwrap())
    //         .collect();
    //     lefties.push(splitted[0]);
    //     righties.push(splitted[1]);
    // }
    // input.iter()
    //     .map(|line| line.split("   "))
    //     .for_each(|mut couple| {
    //         lefties.push(i32::from_str(couple.next().unwrap()).unwrap());
    //         righties.push(i32::from_str(couple.next().unwrap()).unwrap());
    //     });
    input.iter()
        .map(|line| line.split("   ")
                         .map(|item| i32::from_str(item).unwrap())
                         .collect())
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
