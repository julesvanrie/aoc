use std::env;
use std::fs;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input()?;

    solve(input);

    Ok(())
}

fn read_input() -> Result<String, Box<dyn Error>> {
    let args: Vec<String> = env::args().collect();
    let file_name = format!("{}.txt", &args[1]);
    let file_content = fs::read_to_string(file_name)?;
    Ok(file_content.trim().to_string())
}

fn solve(input: String) {
    let mut test = input;

    let mut new: Vec::<u8>;

    loop {
        new = vec![];
        let mut carry = 1;
        for c in test.as_bytes().iter().rev() {
            new.push(match carry {
                0 => *c,
                1 => match c {
                    b'z' => { carry = 1; b'a' },
                    _    => { carry = 0; c + 1 }
                },
                _ => panic!()
            })
        }
        let new_password = String::from_utf8(new.clone().into_iter().rev().collect()).unwrap();

        if is_valid(&new_password) { break }
        test = last_invalid(&new_password).to_string();
    }

    let answer_one = String::from_utf8(new.into_iter().rev().collect());

    println!("The answer for part 1 is: {:?}", answer_one);
}

fn is_valid(password: &String) -> bool {
    // Check no i, o, or l
    if password.contains(|c| match c {
        'i' | 'o' | 'l' => true,
        _ => false
    }) {
        return false;
    }

    // consecutive
    let mut consecutive = false;
    let the_chars = password.as_bytes();
    for i in 0..password.len()-2 {
        if the_chars[i+1] == the_chars[i] + 1 &&
           the_chars[i+2] == the_chars[i] + 2 {
            consecutive = true;
        }
    }

    // pairs
    let mut pairs = 0;
    let mut first_pair = "".as_bytes();
    let the_chars = password.as_bytes();
    for i in 0..password.len()-1 {
        if the_chars[i+1] == the_chars[i]  {
            if first_pair.len() == 0 {
                first_pair = &the_chars[i..i+2];
                pairs = 1;
            } else {
                if the_chars[i..i+2] != *first_pair {
                    pairs += 1;
                }
            }
        }
    }

    if consecutive && pairs >= 2 {
        true
    } else {
        false
    }
}

fn last_invalid(password: &String) -> String {
    let num_chars = password.len();
    if let Some(ix) = password.rfind(|c| match c {
        'i' | 'o' | 'l' => true,
        _ => false
    }) {
        format!(
            "{}{}",
            password.get(0..ix+1).unwrap(),
            String::from_utf8(vec![b'z'; num_chars-ix-1]).unwrap())
    } else {
        password.clone()
    }
}
