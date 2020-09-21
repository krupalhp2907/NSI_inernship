function customJsInterface(object, virtual) {
    virtual.forEach(method => {
        try {
            let func = object[virtual];
        } catch (error) {
            throw Error("cannot instantiate object without " + method + " method");
        }
    });
}

function remove_character(str, char_pos) {
    part1 = str.substring(0, char_pos);
    part2 = str.substring(char_pos + 1, str.length);
    return (part1 + part2);
}

function count_letter(str, letter) {
    let count = 0;
    for (let i = 0; i < str.length; i++) {
        if (str[i] == letter) {
            count += 1;
        }
    }
    return count;
}

function nextGame(num, total) {
    return num % total;
}