#pragma once
#include <algorithm>
#include <cmath>
#include <functional>
#include <iterator>
#include <limits>
#include <random>
#include <vector>


namespace Fortuna {
    using Integer = long long;
    using Float = double;

    static std::random_device hardware_seed;
    static std::shuffle_order_engine<std::discard_block_engine<std::mt19937_64, 12, 8>, 256> hurricane {hardware_seed()};

    auto min_int() -> Integer { return -std::numeric_limits<Integer>::max(); }
    auto max_int() -> Integer { return std::numeric_limits<Integer>::max(); }
    auto min_float() -> Float { return std::numeric_limits<Float>::lowest(); }
    auto max_float() -> Float { return std::numeric_limits<Float>::max(); }
    auto min_below() -> Float { return std::nextafter(0.0, std::numeric_limits<Float>::lowest()); }
    auto min_above() -> Float { return std::nextafter(0.0, std::numeric_limits<Float>::max()); }

    template <typename Number>
    auto smart_clamp(Number target, Number left_limit, Number right_limit) -> Number {
        return std::clamp(target, std::min(left_limit, right_limit), std::max(right_limit, left_limit));
    }

    template <typename Function, typename Number, typename Offset>
    auto analytic_continuation(Function && func, Number number, Offset offset) -> Number {
        if (number > 0) return func(number);
        if (number < 0) return -func(-number) + offset;
        return offset;
    }

    auto generate_canonical() -> Float {
        return std::generate_canonical<Float, std::numeric_limits<Float>::digits>(Fortuna::hurricane);
    }

    auto random_float(Float left_limit, Float right_limit) -> Float {
        std::uniform_real_distribution<Float> distribution { left_limit, right_limit };
        return distribution(Fortuna::hurricane);
    }

    auto random_below(Integer number) -> Integer {
        if (number > 0) {
            std::uniform_int_distribution<Integer> distribution { 0, number - 1 };
            return distribution(Fortuna::hurricane);
        }
        return Fortuna::analytic_continuation(Fortuna::random_below, number, 0);
    }

    auto random_index(Integer number) -> Integer {
        if (number > 0) {
            std::uniform_int_distribution<Integer> distribution { 0, number - 1 };
            return distribution(Fortuna::hurricane);
        }
        return Fortuna::analytic_continuation(Fortuna::random_index, number, -1);
    }

    auto random_int(Integer left_limit, Integer right_limit) -> Integer {
        std::uniform_int_distribution<Integer> distribution {
            std::min(left_limit, right_limit),
            std::max(left_limit, right_limit),
        };
        return distribution(Fortuna::hurricane);
    }

    auto random_range(Integer start, Integer stop, Integer step) -> Integer {
        if (start == stop or step == 0) return start;
        const auto width { std::abs(start - stop) - 1 };
        const auto pivot { step > 0 ? std::min(start, stop) : std::max(start, stop) };
        const auto step_size { std::abs(step) };
        return pivot + step_size * Fortuna::random_below((width + step_size) / step);
    }

    /// RNG
    auto bernoulli(double truth_factor) -> bool {
        std::bernoulli_distribution distribution {
            std::clamp(truth_factor, 0.0, 1.0)
        };
        return distribution(Fortuna::hurricane);
    }

    auto binomial(Integer number_of_trials, double probability) -> Integer {
        std::binomial_distribution<Integer> distribution {
            std::max(number_of_trials, Integer(1)),
            std::clamp(probability, 0.0, 1.0),
        };
        return distribution(Fortuna::hurricane);
    }

    auto negative_binomial(Integer number_of_trials, double probability) -> Integer {
        std::negative_binomial_distribution<Integer> distribution {
            std::max(number_of_trials, Integer(1)),
            std::clamp(probability, 0.0, 1.0)
        };
        return distribution(Fortuna::hurricane);
    }

    auto geometric(double probability) -> Integer {
        std::geometric_distribution<Integer> distribution { std::clamp(probability, 0.0, 1.0) };
        return distribution(Fortuna::hurricane);
    }

    auto poisson(double mean) -> Integer {
        std::poisson_distribution<Integer> distribution { mean };
        return distribution(Fortuna::hurricane);
    }

    auto expovariate(Float lambda_rate) -> Float {
        std::exponential_distribution<Float> distribution { lambda_rate };
        return distribution(Fortuna::hurricane);
    }

    auto gammavariate(Float shape, Float scale) -> Float {
        std::gamma_distribution<Float> distribution { shape, scale };
        return distribution(Fortuna::hurricane);
    }

    auto weibullvariate(Float shape, Float scale) -> Float {
        std::weibull_distribution<Float> distribution { shape, scale };
        return distribution(Fortuna::hurricane);
    }

    auto normalvariate(Float mean, Float std_dev) -> Float {
        std::normal_distribution<Float> distribution { mean, std_dev };
        return distribution(Fortuna::hurricane);
    }

    auto lognormvariate(Float log_mean, Float log_deviation) -> Float {
        std::lognormal_distribution<Float> distribution { log_mean, log_deviation };
        return distribution(Fortuna::hurricane);
    }

    auto extreme_value(Float location, Float scale) -> Float {
        std::extreme_value_distribution<Float> distribution { location, scale };
        return distribution(Fortuna::hurricane);
    }

    auto chi_squared(Float degrees_of_freedom) -> Float {
        std::chi_squared_distribution<Float> distribution {
            std::max(degrees_of_freedom, Float(0.0))
        };
        return distribution(Fortuna::hurricane);
    }

    auto cauchy(Float location, Float scale) -> Float {
        std::cauchy_distribution<Float> distribution { location, scale };
        return distribution(Fortuna::hurricane);
    }

    auto fisher_f(Float degrees_of_freedom_1, Float degrees_of_freedom_2) -> Float {
        std::fisher_f_distribution<Float> distribution {
            std::max(degrees_of_freedom_1, Float(0.0)),
            std::max(degrees_of_freedom_2, Float(0.0))
        };
        return distribution(Fortuna::hurricane);
    }

    auto student_t(Float degrees_of_freedom) -> Float {
        std::student_t_distribution<Float> distribution {
            std::max(degrees_of_freedom, Float(0.0))
        };
        return distribution(Fortuna::hurricane);
    }

    /// Pyewacket
    auto betavariate(Float alpha, Float beta) -> Float {
        const auto y { Fortuna::gammavariate(alpha, 1.0) };
        if (y == 0) return 0.0;
        return y / (y + Fortuna::gammavariate(beta, 1.0));
    }

    auto paretovariate(Float alpha) -> Float {
        const auto u { 1.0 - Fortuna::generate_canonical() };
        return 1.0 / std::pow(u, 1.0 / alpha);
    }

    auto vonmisesvariate(Float mu, Float kappa) -> Float {
        static const auto PI { 4 * std::atan(1) };
        static const auto TAU { 8 * std::atan(1) };
        if (kappa <= 0.000001) return TAU * Fortuna::generate_canonical();
        const auto s { 0.5 / kappa };
        const auto r { s + std::sqrt(1 + s * s) };
        auto u1 {0};
        auto z {0};
        auto d {0};
        auto u2 {0};
        while (true) {
            u1 = Fortuna::generate_canonical();
            z = std::cos(PI * u1);
            d = z / (r + z);
            u2 = Fortuna::generate_canonical();
            if (u2 < 1.0 - d * d or u2 <= (1.0 -d) * std::exp(d)) break;
        }
        const auto q { 1.0 / r };
        const auto f { (q + z) / (1.0 + q * z) };
        const auto u3 { Fortuna::generate_canonical() };
        if (u3 > 0.5) return std::fmod(mu + std::acos(f), TAU);
        return std::fmod(mu - std::acos(f), TAU);
    }

    auto triangular(Float low, Float high, Float mode) -> Float {
        if (high - low == 0) return low;
        auto u { Fortuna::generate_canonical() };
        auto c { (mode - low) / (high - low) };
        if (u > c) {
            u = 1.0 - u;
            c = 1.0 - c;
            const auto temp = low;
            low = high;
            high = temp;
        }
        return low + (high - low) * std::sqrt(u * c);
    }

    /// Fortuna
    auto percent_true(Float truth_factor) -> bool {
        return Fortuna::random_float(0.0, 100.0) < truth_factor;
    }

    auto d(Integer sides) -> Integer {
        if (sides > 0) {
            std::uniform_int_distribution<Integer> distribution {1, sides};
            return distribution(Fortuna::hurricane);
        }
        return analytic_continuation(d, sides, 0);
    }

    auto dice(Integer rolls, Integer sides) -> Integer {
        if (rolls > 0) {
            auto total {0};
            for (auto i {0}; i < rolls; ++i) total += d(sides);
            return total;
        }
        return -dice(-rolls, sides);
    }

    auto dice_algo(Integer rolls, Integer sides) -> Integer {
        if (rolls > 0) {
            std::vector<Integer> the_rolls(rolls);
            std::generate_n(the_rolls.begin(), rolls, [&sides]() { return d(sides); });
            return std::reduce(the_rolls.cbegin(), the_rolls.cend());
        }
        return -dice_algo(-rolls, sides);
    }

     auto ability_dice(Integer number) -> Integer {
        const Integer num { std::clamp(number, Integer(3), Integer(9)) };
        if (num == 3) return dice(3, 6);
        std::vector<Integer> the_rolls(num);
        std::generate_n(the_rolls.begin(), num, []() { return d(6); });
        std::partial_sort(the_rolls.begin(), the_rolls.begin() + 3, the_rolls.end(), std::greater<>());
        return std::reduce(the_rolls.cbegin(), the_rolls.cbegin() + 3);
    }

    auto plus_or_minus(Integer number) -> Integer {
        return random_int(-number, number);
    }

    auto plus_or_minus_linear(Integer number) -> Integer {
        const auto num { std::abs(number) };
        return dice(2, num + 1) - (num + 2);
    }

    auto plus_or_minus_gauss(Integer number) -> Integer {
        static const auto PI { 4 * std::atan(1) };
        const auto num { std::abs(number) };
        const auto result { Integer(std::round(Fortuna::normalvariate(0.0, num / PI))) };
        if (result >= -num and result <= num) return result;
        return Fortuna::plus_or_minus_linear(num);
    }

    auto fuzzy_clamp(Integer target, Integer upper_bound) -> Integer {
        if (target >= 0 and target < upper_bound) return target;
        return Fortuna::random_index(upper_bound);
    }

    /// ZeroCool Methods
    auto back_gauss(Integer) -> Integer;
    auto front_gauss(Integer number) -> Integer {
        if (number > 0) {
            const auto result { Integer(std::floor(Fortuna::gammavariate(1.0, number / 10.0))) };
            return Fortuna::fuzzy_clamp(result, number);
        }
        return Fortuna::analytic_continuation(back_gauss, number, -1);
    }

    auto middle_gauss(Integer number) -> Integer {
        if (number > 0) {
            const auto result { Integer(std::floor(Fortuna::normalvariate(number / 2.0, number / 10.0))) };
            return Fortuna::fuzzy_clamp(result, number);
        }
        return Fortuna::analytic_continuation(middle_gauss, number, -1);
    }

    auto back_gauss(Integer number) -> Integer {
        if (number > 0) {
            return number - Fortuna::front_gauss(number) - 1;
        }
        return Fortuna::analytic_continuation(front_gauss, number, -1);
    }

    auto quantum_gauss(Integer number) -> Integer {
        const auto rand_num { Fortuna::d(3) };
        if (rand_num == 1) return Fortuna::front_gauss(number);
        if (rand_num == 2) return Fortuna::middle_gauss(number);
        return Fortuna::back_gauss(number);
    }

    auto back_poisson(Integer) -> Integer;
    auto front_poisson(Integer number) -> Integer {
        if (number > 0) {
            const auto result { Fortuna::poisson(number / 4.0) };
            return Fortuna::fuzzy_clamp(result, number);
        }
        return Fortuna::analytic_continuation(back_poisson, number, -1);
    }

    auto back_poisson(Integer number) -> Integer {
        if (number > 0) {
            const auto result { number - Fortuna::front_poisson(number) - 1 };
            return Fortuna::fuzzy_clamp(result, number);
        }
        return Fortuna::analytic_continuation(front_poisson, number, -1);
    }

    auto middle_poisson(Integer number) -> Integer {
        if (Fortuna::percent_true(50)) return Fortuna::front_poisson(number);
        return Fortuna::back_poisson(number);
    }

    auto quantum_poisson(Integer number) -> Integer {
        const auto rand_num { Fortuna::d(3) };
        if (rand_num == 1) return Fortuna::front_poisson(number);
        if (rand_num == 2) return Fortuna::middle_poisson(number);
        return Fortuna::back_poisson(number);
    }

    auto back_linear(Integer) -> Integer;
    auto front_linear(Integer number) -> Integer {
        if (number > 0) {
            return Fortuna::triangular(0, number, 0);
        }
        return Fortuna::analytic_continuation(back_linear, number, -1);
    }

    auto back_linear(Integer number) -> Integer {
        if (number > 0) {
            return Fortuna::triangular(0, number, number);
        }
        return Fortuna::analytic_continuation(front_linear, number, -1);
    }

    auto middle_linear(Integer number) -> Integer {
        if (number > 0) {
            return Fortuna::triangular(0, number, number / 2.0);
        }
        return Fortuna::analytic_continuation(middle_linear, number, -1);
    }

    auto quantum_linear(Integer number) -> Integer {
        const auto rand_num { Fortuna::d(3) };
        if (rand_num == 1) return Fortuna::front_linear(number);
        if (rand_num == 2) return Fortuna::middle_linear(number);
        return Fortuna::back_linear(number);
    }

    auto quantum_monty(Integer number) -> Integer {
        const auto rand_num { Fortuna::d(3) };
        if (rand_num == 1) return Fortuna::quantum_linear(number);
        if (rand_num == 2) return Fortuna::quantum_gauss(number);
        return Fortuna::quantum_poisson(number);
    }

    /// Generators
    template<typename Value>
    auto random_value(const std::vector<Value> & data) -> Value {
        return data[Fortuna::random_index(data.size())];
    }

    template<typename Value, typename ZeroCool>
    auto random_value(const std::vector<Value> & data, ZeroCool zero_cool) -> Value {
        return data[zero_cool(data.size())];
    }

    template<typename Value, typename ZeroCool>
    auto random_value(const std::vector<Value> & data, ZeroCool zero_cool, int range) -> Value {
        if (range > 0) return data[zero_cool(range)];
        if (range < 0) return data[zero_cool(range) + data.size()];
        return data[zero_cool(data.size())];
    }

    template<typename Value>
    struct TruffleShuffle {
        TruffleShuffle(std::vector<Value> values) : values(values) {
            std::shuffle(values.begin(), values.end(), Fortuna::hurricane);
        }
        auto operator()() -> Value {
            if (values.size() == 1) return values.front();
            return random_rotate(values, Fortuna::front_poisson);
        }
      private:
        std::vector<Value> values;
        template<typename ZeroCool>
        auto random_rotate(std::vector<Value> & values, ZeroCool && func) -> Value {
            auto pivot { values.begin() + 1 + func(values.size() - 1) };
            return * std::rotate(values.begin(), pivot, values.end());
        }
    };

    template<typename Weight>
    auto cumulative_from_relative(const std::vector<Weight> & rel_weights) -> std::vector<Weight> {
        std::vector<Weight> cum_weights(rel_weights.size());
        std::partial_sum(rel_weights.cbegin(), rel_weights.cend(), cum_weights.begin());
        return cum_weights;
    }

    template<typename Weight>
    auto relative_from_cumulative(const std::vector<Weight> & cum_weights) -> std::vector<Weight> {
        std::vector<Weight> rel_weights(cum_weights.size());
        std::adjacent_difference(cum_weights.cbegin(), cum_weights.cend(), rel_weights.begin());
        return rel_weights;
    }

    template<typename Weight, typename Value>
    auto cumulative_weighted_choice(const std::vector<Weight> & weights, const std::vector<Value> & values) -> Value {
        const auto max_weight { weights.back() };
        const auto raw_weight { Fortuna::random_float(0.0, max_weight) };
        const auto valid_weight { std::lower_bound(weights.cbegin(), weights.cend(), raw_weight) };
        const auto result_idx { std::distance(weights.cbegin(), valid_weight) };
        return values[result_idx];
    }

} // end Fortuna namespace
