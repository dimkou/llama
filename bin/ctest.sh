#!/bin/sh

# Check that no conflicts arised during grammar processing.
! grep "conflict" --silent ./tables/parser.out
