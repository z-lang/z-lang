-- boolean operations
z_true = True
z_false = False
z_and(a, b) = and [a, b]
z_or(a, b) = or [a, b]
z_not(a) = not a

--z_case :: (Bool, a, a) -> a
z_case(True, a, b) = a
z_case(False, a, b) = b

-- arithmetic operations
z_add(a, b) = a + b
z_sub(a, b) = a - b
z_mul(a, b) = a * b
z_div(a, b) = div a b
z_mod(a, b) = mod a b
z_eq(a, b)  = a == b
z_ne(a, b)  = a /= b
z_le(a, b)  = a <= b
z_ge(a, b)  = a >= b
z_lt(a, b)  = a < b
z_gt(a, b)  = a > b

-- list functions
z_len(l) = length(l)

--z_get :: ([a], Int) -> a
z_get(l, i) = l!!i

--z_join :: ([a], [a]) -> [a]
z_join(a, b) = a ++ b

--z_tail :: [a] -> [a]
z_tail x = tail(x)

