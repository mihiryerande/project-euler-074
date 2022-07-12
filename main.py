# Problem 74:
#     Digit Factorial Chains
#
# Description:
#     The number 145 is well known for the property that the sum of the factorial of its digits is equal to 145:#
#         1! + 4! + 5! = 1 + 24 + 120 = 145
#
#     Perhaps less well known is 169, in that it produces the longest chain of numbers that link back to 169;
#       it turns out that there are only three such loops that exist:
#         169 → 363601 → 1454 → 169
#         871 → 45361 → 871
#         872 → 45362 → 872
#
#     It is not difficult to prove that EVERY starting number will eventually get stuck in a loop.
#     For example,
#         69 → 363600 → 1454 → 169 → 363601 (→ 1454)
#         78 → 45360 → 871 → 45361 (→ 871)
#         540 → 145 (→ 145)
#
#     Starting with 69 produces a chain of five non-repeating terms,
#       but the longest non-repeating chain with a starting number below one million is sixty terms.
#
#     How many chains, with a starting number below one million, contain exactly sixty non-repeating terms?

def main(n: int) -> int:
    """
    Returns the number of digit-factorial-chains with a starting number below `n` having exactly 60 distinct terms.

    Args:
        n (int): Natural number

    Returns:
        (int): Number of chains starting below `n` with 60 distinct terms.

    Raises:
        AssertError: if incorrect args are given
    """
    assert type(n) == int and n > 0

    # Calculate digit factorials once and store for later
    f = [1]
    for i in range(1, 10):
        f.append(f[-1]*i)

    # Function to get next number in digit-factorial-chain
    def chain_next(x):
        return sum(map(lambda d: f[int(d)], list(str(x))))

    # Store lengths of chains starting at already-seen numbers
    chain_lengths = dict()

    # Seed with (all?) known self-looping numbers, and their loop-lengths,
    #   to know when to terminate chains once they start looping
    loop_seeds = [1, 2, 145, 169, 871, 872, 40585]
    for loop_seed in loop_seeds:
        loop_members = []
        chain_curr = loop_seed
        while True:
            loop_members.append(chain_curr)
            chain_curr = chain_next(chain_curr)
            if chain_curr == loop_seed:
                break
        loop_length = len(loop_members)
        for loop_member in loop_members:
            chain_lengths[loop_member] = loop_length

    sixty_count = 0
    for starter in range(1, n):
        # Count chain elements until hitting already-seen element
        chain_curr = starter
        chain = []
        chain_length = 0
        while chain_curr not in chain_lengths:
            chain.append(chain_curr)
            chain_length += 1
            chain_curr = chain_next(chain_curr)

        # Add the remaining chain length using already-seen element
        chain_length += chain_lengths[chain_curr]
        sixty_count += (chain_length == 60)

        # Cache chain-lengths starting at all new elements seen in this chain,
        #   to avoid redundant iteration in later chains
        while len(chain) > 0:
            chain_lengths[chain.pop(0)] = chain_length
            chain_length -= 1

    return sixty_count


if __name__ == '__main__':
    starting_bound = int(input('Enter a natural number: '))
    large_chain_count = main(starting_bound)
    print('Number of digit-factorial-chains starting below {}, with exactly 60 distinct terms:'.format(starting_bound))
    print('  {}'.format(large_chain_count))
