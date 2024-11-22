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
    let mut counter = 0;
    let mut one_found = false;
    loop {
        counter += 1;
        let hash_input = format!("{}{}", input, counter);
        let hash = md5::compute(hash_input);

        if !one_found && format!("{:x}", hash)[0..5] == *"00000" {
            println!("The answer for part 1 is: {}", counter);
            one_found = true;
        }
        if format!("{:x}", hash)[0..6] == *"000000" {
            println!("The answer for part 2 is: {}", counter);
            break
        }
    }
}
