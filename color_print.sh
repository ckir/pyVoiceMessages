#!/bin/bash

printGray() {
    printf "\e[38;5;8m%s\e[0m" "$1"
    echo ""
}

printRed() {
    printf "\e[38;5;9m%s\e[0m" "$1"
    echo ""
}

printGreen() {
    printf "\e[38;5;10m%s\e[0m" "$1"
    echo ""
}

printYellow() {
    printf "\e[38;5;11m%s\e[0m" "$1"
    echo ""
}

printBlue() {
    printf "\e[38;5;12m%s\e[0m" "$1"
    echo ""
}

printWMagenta() {
    printf "\e[38;5;13m%s\e[0m" "$1"
    echo ""
}

printCyan() {
    printf "\e[38;5;14m%s\e[0m" "$1"
    echo ""
}

printWhite() {
    printf "\e[38;5;15m%s\e[0m" "$1"
    echo ""
}