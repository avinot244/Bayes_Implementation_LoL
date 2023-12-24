#!/bin/bash


# Function to list directories recursively given a max depth
list_directories_recursive(){
    local current_dir="$1"
    local local_depth="$2"
    local max_depth="$3"
    local result=()
    local tempRes=$current_dir

    # Looping through dirs in the current directory
    for item in "$current_dir"/*; do
        
        if [ -d "$item" ]; then
            # Recursively call the function for subdirectories
            local_depth=$(expr $local_depth + 1)
            # echo "item $item local_depth $local_depth"
            if [ $local_depth -lt $max_depth ]; then
                
                
                list_directories_recursive "$item" $local_depth $max_depth
            fi
            result+=($item)
        fi
        local_depth=0
    done
    echo ${result[@]}
}

split_string() {
    local s="$1"
    local d="$2"

    # Set IFS (Internal Field Separator) to the delimiter
    IFS="$d"

    # Create an array by splitting the string
    read -ra parts <<< "$s"

    # Return the array
    echo "${parts[@]}"
}


replace_yaml_value() {
    local file="$1"
    local key="$2"
    local new_value="$3"

    # Check if the file exists
    if [ ! -f "$file" ]; then
        echo "Error: File not found."
        exit 1
    fi

    # Use awk to find and replace the value associated with the key
    awk -v key="$key" -v new_value="$new_value" '
        BEGIN {
            FS=": "; OFS=": ";
        }
        $1 == key {
            $2 = new_value;
        }
        { print }
    ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"

}

# Start the recursive listing from the current directory
paths=($(list_directories_recursive "../data" 0 1))
delimiter="/"
for path in ${paths[@]}; do

    result=($(split_string "$path" "$delimiter"))
    matchName=${result[2]}
    replace_yaml_value "config.yml" "match" "$matchName"

    python3 main.py --draft --game 1
done

# for matchNumber in "113188" "112248" "113183" "113180" "112229" "113164" "113155" "113151" "113144" "113168" do
#     matchName="LOLMNT99_$matchNumber"
#     replace_yaml_value "config.yml" "match" "$matchName"
#     python3 main.py --draft --game 1
# done