#!/bin/bash
for file in $(<pipelineneustart_1.txt); do cp "$file" ./fastasCont/; done
