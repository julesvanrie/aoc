use std::env;
use std::fs;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input()?;

    solve(&input);

    Ok(())
}

fn read_input() -> Result<String, Box<dyn Error>> {
    let args: Vec<String> = env::args().collect();
    let file_name = format!("{}.txt", &args[1]);
    let file_content = fs::read_to_string(file_name)?;
    Ok(file_content.trim().to_string())
}

fn solve(input: &str) {
    let mut numbers: Vec<u32> = input.chars().map(|b| b.to_digit(10).unwrap()).collect();

    for i in 0..50 {
        let mut new = vec![];
        let mut prev = numbers[0];
        let mut count = 1;
        for number in &numbers[1..] {
            match *number == prev {
                true => count += 1,
                false => {
                    new.push(count);
                    new.push(prev);
                    count = 1;
                    prev = *number;
                }
            }

        }
        new.push(count);
        new.push(prev);

        match i {
            39 => println!("The answer for part 1 is: {}", new.len()),
            49 => println!("The answer for part 2 is: {}", new.len()),
            _ => ()
        }

        numbers = new;
    }
}
