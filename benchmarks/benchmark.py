from censore import ProfanityFilter
import time

pf = ProfanityFilter(languages=["en"])

profane_text = " ".join(["fuck"] * 100)

# Start timing
start_time = time.time()

# Censor the words
pf.censor(profane_text)

# End timing
end_time = time.time()

# Print the time taken
print(f"Time taken to censor 100 words: {end_time - start_time} seconds")
