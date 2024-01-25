for dir in abgabe*/; do
    python3 -m unittest discover -s "$dir"
done