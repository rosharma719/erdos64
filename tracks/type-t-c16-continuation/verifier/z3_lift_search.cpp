// Exhaustive normalized cyclic Z3-lift search for the four certified bases.
//
// The search space is deliberately not quotiented: assignment index a in
// [0,3^13) is the base-3 voltage vector with coordinate 0 least significant.
// Tree edges have voltage zero.  Exact simple-cycle tests are staged at
// lengths 4,8,16,32,64.

#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <queue>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {

constexpr int BASE_N = 24;
constexpr int BASE_M = 36;
constexpr int LIFT_N = 72;
constexpr int COTREE_RANK = 13;
constexpr std::uint32_t ASSIGNMENTS = 1594323;  // 3^13

struct Bits {
    std::uint64_t lo = 0;
    std::uint64_t hi = 0;
    bool has(int v) const {
        return v < 64 ? ((lo >> v) & 1U) : ((hi >> (v - 64)) & 1U);
    }
    void add(int v) {
        if (v < 64) lo |= std::uint64_t{1} << v;
        else hi |= std::uint64_t{1} << (v - 64);
    }
    void remove(int v) {
        if (v < 64) lo &= ~(std::uint64_t{1} << v);
        else hi &= ~(std::uint64_t{1} << (v - 64));
    }
};

struct Graph72 {
    std::array<std::array<int, 3>, LIFT_N> adj{};
    std::array<int, LIFT_N> degree{};

    void add_edge(int u, int v) {
        if (u == v || degree[u] >= 3 || degree[v] >= 3)
            throw std::runtime_error("invalid lifted edge");
        for (int i = 0; i < degree[u]; ++i)
            if (adj[u][i] == v) throw std::runtime_error("parallel lifted edge");
        adj[u][degree[u]++] = v;
        adj[v][degree[v]++] = u;
    }

    void finish() {
        for (int v = 0; v < LIFT_N; ++v) {
            if (degree[v] != 3) throw std::runtime_error("lift is not cubic");
            std::sort(adj[v].begin(), adj[v].end());
        }
    }
};

struct Base {
    std::array<std::pair<int, int>, BASE_M> edges{};
    std::array<std::pair<int, int>, COTREE_RANK> cotree{};
};

Base read_base(const std::string& path) {
    std::ifstream input(path);
    if (!input) throw std::runtime_error("cannot open base edge list: " + path);
    int n = 0, m = 0;
    input >> n >> m;
    if (n != BASE_N || m != BASE_M) throw std::runtime_error("unexpected base size");
    Base base;
    std::array<std::vector<int>, BASE_N> adjacency;
    for (int i = 0; i < BASE_M; ++i) {
        int u = -1, v = -1;
        input >> u >> v;
        if (!input || u < 0 || u >= v || v >= BASE_N)
            throw std::runtime_error("invalid canonical base edge");
        base.edges[i] = {u, v};
        adjacency[u].push_back(v);
        adjacency[v].push_back(u);
    }
    for (auto& neighbors : adjacency) std::sort(neighbors.begin(), neighbors.end());

    std::array<bool, BASE_N> seen{};
    std::array<std::array<bool, BASE_N>, BASE_N> tree{};
    std::queue<int> queue;
    seen[0] = true;
    queue.push(0);
    int tree_count = 0;
    while (!queue.empty()) {
        int u = queue.front();
        queue.pop();
        for (int v : adjacency[u]) {
            if (!seen[v]) {
                seen[v] = true;
                queue.push(v);
                tree[u][v] = tree[v][u] = true;
                ++tree_count;
            }
        }
    }
    if (tree_count != BASE_N - 1) throw std::runtime_error("base is disconnected");
    int coordinate = 0;
    for (auto edge : base.edges) {
        if (!tree[edge.first][edge.second]) {
            if (coordinate >= COTREE_RANK) throw std::runtime_error("cycle rank exceeds 13");
            base.cotree[coordinate++] = edge;
        }
    }
    if (coordinate != COTREE_RANK) throw std::runtime_error("cycle rank is not 13");
    return base;
}

std::array<int, COTREE_RANK> decode_assignment(std::uint32_t index) {
    std::array<int, COTREE_RANK> values{};
    for (int i = 0; i < COTREE_RANK; ++i) {
        values[i] = static_cast<int>(index % 3);
        index /= 3;
    }
    return values;
}

Graph72 make_lift(const Base& base, std::uint32_t assignment) {
    auto values = decode_assignment(assignment);
    Graph72 graph;
    for (auto [u, v] : base.edges) {
        int voltage = 0;
        for (int coordinate = 0; coordinate < COTREE_RANK; ++coordinate) {
            if (base.cotree[coordinate] == std::pair<int, int>{u, v}) {
                voltage = values[coordinate];
                break;
            }
        }
        for (int sheet = 0; sheet < 3; ++sheet)
            graph.add_edge(3 * u + sheet, 3 * v + (sheet + voltage) % 3);
    }
    graph.finish();
    return graph;
}

bool adjacent(const Graph72& graph, int u, int v) {
    for (int neighbor : graph.adj[u])
        if (neighbor == v) return true;
    return false;
}

bool find_c4(const Graph72& graph, std::vector<int>& witness) {
    for (int u = 0; u < LIFT_N; ++u) {
        for (int v = u + 1; v < LIFT_N; ++v) {
            int common[2] = {-1, -1};
            int count = 0;
            for (int a : graph.adj[u]) {
                if (adjacent(graph, v, a) && count < 2) common[count++] = a;
            }
            if (count == 2) {
                witness = {u, common[0], v, common[1]};
                return true;
            }
        }
    }
    return false;
}

struct CycleSearch {
    const Graph72& graph;
    int target = 0;
    int root = 0;
    int first = 0;
    Bits visited;
    std::vector<int> path;
    std::vector<int> witness;

    explicit CycleSearch(const Graph72& input) : graph(input) {}

    bool dfs(int current) {
        int used = static_cast<int>(path.size());
        if (used == target) {
            if (first < current && adjacent(graph, current, root)) {
                witness = path;
                return true;
            }
            return false;
        }
        for (int next : graph.adj[current]) {
            if (next <= root || visited.has(next)) continue;
            visited.add(next);
            path.push_back(next);
            if (dfs(next)) return true;
            path.pop_back();
            visited.remove(next);
        }
        return false;
    }

    bool run(int length) {
        target = length;
        witness.clear();
        if (length < 3 || length > LIFT_N) return false;
        for (root = 0; root <= LIFT_N - length; ++root) {
            for (int neighbor : graph.adj[root]) {
                if (neighbor <= root) continue;
                first = neighbor;
                visited = {};
                visited.add(root);
                visited.add(neighbor);
                path = {root, neighbor};
                if (dfs(neighbor)) return true;
            }
        }
        return false;
    }
};

std::string vector_json(const std::vector<int>& values) {
    std::ostringstream output;
    output << '[';
    for (std::size_t i = 0; i < values.size(); ++i) {
        if (i) output << ',';
        output << values[i];
    }
    output << ']';
    return output.str();
}

std::string assignment_json(std::uint32_t index) {
    auto values = decode_assignment(index);
    return vector_json(std::vector<int>(values.begin(), values.end()));
}

struct Sample {
    bool set = false;
    std::uint32_t assignment = 0;
    std::vector<int> cycle;
};

struct Options {
    std::string base_path;
    std::string output_path;
    std::string survivor_prefix;
    int base_index = -1;
    std::uint32_t start = 0;
    std::uint32_t end = ASSIGNMENTS;
};

Options parse_options(int argc, char** argv) {
    Options options;
    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (i + 1 >= argc) throw std::runtime_error("missing value for " + arg);
        std::string value = argv[++i];
        if (arg == "--base") options.base_path = value;
        else if (arg == "--base-index") options.base_index = std::stoi(value);
        else if (arg == "--start") options.start = static_cast<std::uint32_t>(std::stoul(value));
        else if (arg == "--end") options.end = static_cast<std::uint32_t>(std::stoul(value));
        else if (arg == "--output") options.output_path = value;
        else if (arg == "--survivor-prefix") options.survivor_prefix = value;
        else throw std::runtime_error("unknown option: " + arg);
    }
    if (options.base_path.empty() || options.output_path.empty() ||
        options.survivor_prefix.empty() || options.base_index < 0)
        throw std::runtime_error("required: --base --base-index --output --survivor-prefix");
    if (options.start > options.end || options.end > ASSIGNMENTS)
        throw std::runtime_error("invalid half-open assignment range");
    return options;
}

}  // namespace

int main(int argc, char** argv) {
    try {
        Options options = parse_options(argc, argv);
        Base base = read_base(options.base_path);
        std::ofstream after8(options.survivor_prefix + ".after8.txt");
        std::ofstream after16(options.survivor_prefix + ".after16.txt");
        std::ofstream after32(options.survivor_prefix + ".after32.txt");
        std::ofstream after64(options.survivor_prefix + ".after64.txt");
        if (!after8 || !after16 || !after32 || !after64)
            throw std::runtime_error("cannot create survivor output files");

        std::array<std::uint64_t, 5> survivors{};
        std::array<double, 5> stage_seconds{};
        std::array<Sample, 5> rejection_samples{};
        std::uint64_t examined = 0;
        auto started = std::chrono::steady_clock::now();

        for (std::uint32_t assignment = options.start; assignment < options.end; ++assignment) {
            if (assignment == 0) continue;  // disconnected trivial lift
            ++examined;
            Graph72 graph = make_lift(base, assignment);
            std::vector<int> witness;
            auto stage_started = std::chrono::steady_clock::now();
            bool found = find_c4(graph, witness);
            stage_seconds[0] += std::chrono::duration<double>(
                std::chrono::steady_clock::now() - stage_started).count();
            if (found) {
                if (!rejection_samples[0].set)
                    rejection_samples[0] = {true, assignment, witness};
                continue;
            }
            ++survivors[0];

            CycleSearch search(graph);
            stage_started = std::chrono::steady_clock::now();
            found = search.run(8);
            stage_seconds[1] += std::chrono::duration<double>(
                std::chrono::steady_clock::now() - stage_started).count();
            if (found) {
                if (!rejection_samples[1].set)
                    rejection_samples[1] = {true, assignment, search.witness};
                continue;
            }
            ++survivors[1];
            after8 << assignment << '\n';

            stage_started = std::chrono::steady_clock::now();
            found = search.run(16);
            stage_seconds[2] += std::chrono::duration<double>(
                std::chrono::steady_clock::now() - stage_started).count();
            if (found) {
                if (!rejection_samples[2].set)
                    rejection_samples[2] = {true, assignment, search.witness};
                continue;
            }
            ++survivors[2];
            after16 << assignment << '\n';

            stage_started = std::chrono::steady_clock::now();
            found = search.run(32);
            stage_seconds[3] += std::chrono::duration<double>(
                std::chrono::steady_clock::now() - stage_started).count();
            if (found) {
                if (!rejection_samples[3].set)
                    rejection_samples[3] = {true, assignment, search.witness};
                continue;
            }
            ++survivors[3];
            after32 << assignment << '\n';

            stage_started = std::chrono::steady_clock::now();
            found = search.run(64);
            stage_seconds[4] += std::chrono::duration<double>(
                std::chrono::steady_clock::now() - stage_started).count();
            if (found) {
                if (!rejection_samples[4].set)
                    rejection_samples[4] = {true, assignment, search.witness};
                continue;
            }
            ++survivors[4];
            after64 << assignment << '\n';
        }

        double seconds = std::chrono::duration<double>(
            std::chrono::steady_clock::now() - started).count();
        const int lengths[5] = {4, 8, 16, 32, 64};
        std::ostringstream json;
        json << "{\n"
             << "  \"schema\": \"erdos64-z3-lift-shard-v1\",\n"
             << "  \"base_index\": " << options.base_index << ",\n"
             << "  \"base_path\": \"" << options.base_path << "\",\n"
             << "  \"assignment_range\": [" << options.start << ',' << options.end << "],\n"
             << "  \"zero_assignment_excluded\": true,\n"
             << "  \"assignments_examined\": " << examined << ",\n"
             << "  \"survivors\": {\n";
        for (int i = 0; i < 5; ++i) {
            json << "    \"" << lengths[i] << "\": " << survivors[i]
                 << (i == 4 ? "\n" : ",\n");
        }
        json << "  },\n  \"stage_seconds\": {\n";
        for (int i = 0; i < 5; ++i) {
            json << "    \"" << lengths[i] << "\": " << std::fixed
                 << std::setprecision(6) << stage_seconds[i]
                 << (i == 4 ? "\n" : ",\n");
        }
        json << "  },\n  \"first_rejection_witnesses\": {\n";
        for (int i = 0; i < 5; ++i) {
            json << "    \"" << lengths[i] << "\": ";
            if (!rejection_samples[i].set) json << "null";
            else {
                const Sample& sample = rejection_samples[i];
                json << "{\"assignment\":" << sample.assignment
                     << ",\"voltage_vector\":" << assignment_json(sample.assignment)
                     << ",\"cycle\":" << vector_json(sample.cycle) << '}';
            }
            json << (i == 4 ? "\n" : ",\n");
        }
        json << "  },\n"
             << "  \"elapsed_seconds\": " << std::fixed << std::setprecision(6) << seconds << ",\n"
             << "  \"assignments_per_second\": "
             << (seconds > 0 ? examined / seconds : 0.0) << "\n}\n";

        std::ofstream output(options.output_path);
        if (!output) throw std::runtime_error("cannot create shard summary");
        output << json.str();
        std::cout << json.str();
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "z3_lift_search: " << error.what() << '\n';
        return 2;
    }
}
