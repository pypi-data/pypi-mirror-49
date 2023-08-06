#include <utility>

#ifndef KRATOS_MODULE_HH
#define KRATOS_MODULE_HH
#include <map>
#include <string>
#include <unordered_map>
#include <vector>

#include "context.hh"
#include "port.hh"

namespace kratos {

class Generator : public std::enable_shared_from_this<Generator>, public IRNode {
public:
    std::string name;
    std::string instance_name;

    static Generator from_verilog(Context *context, const std::string &src_file,
                                  const std::string &top_name,
                                  const std::vector<std::string> &lib_files,
                                  const std::map<std::string, PortType> &port_types);

    Generator(Context *context, const std::string &name)
        : IRNode(IRNodeKind::GeneratorKind), name(name), instance_name(name), context_(context) {}

    Var &var(const std::string &var_name, uint32_t width, uint32_t size);
    Var &var(const std::string &var_name, uint32_t width) { return var(var_name, width, 1); }
    Var &var(const std::string &var_name, uint32_t width, uint32_t size, bool is_signed);
    Port &port(PortDirection direction, const std::string &port_name, uint32_t width) {
        return port(direction, port_name, width, 1);
    }
    Port &port(PortDirection direction, const std::string &port_name, uint32_t width,
               uint32_t size);
    Port &port(PortDirection direction, const std::string &port_name, uint32_t width, uint32_t size,
               PortType type, bool is_signed);
    PortPacked &port_packed(PortDirection direction, const std::string &port_name,
                            const PackedStruct &packed_struct_);
    Const &constant(int64_t value, uint32_t width);
    Const &constant(int64_t value, uint32_t width, bool is_signed);
    Param &parameter(const std::string &parameter_name, uint32_t width);
    Param &parameter(const std::string &parameter_name, uint32_t width, bool is_signed);

    Expr &expr(ExprOp op, const std::shared_ptr<Var> &left, const std::shared_ptr<Var> &right);

    // ports and vars
    std::shared_ptr<Port> get_port(const std::string &port_name);
    std::shared_ptr<Var> get_var(const std::string &var_name);
    const std::set<std::string> &get_port_names() const { return ports_; }
    const std::map<std::string, std::shared_ptr<Var>> &vars() const { return vars_; }
    void remove_var(const std::string &var_name) {
        if (vars_.find(var_name) != vars_.end()) vars_.erase(var_name);
    }
    bool has_port(const std::string &port_name) { return ports_.find(port_name) != ports_.end(); }
    bool has_var(const std::string &var_name) { return vars_.find(var_name) != vars_.end(); }
    void remove_port(const std::string &port_name);
    void rename_var(const std::string &old_name, const std::string &new_name);
    const inline std::map<std::string, std::shared_ptr<Param>> &get_params() const {
        return params_;
    }
    std::shared_ptr<Param> get_param(const std::string &param_name) const;

    // statements
    void add_stmt(std::shared_ptr<Stmt> stmt);
    uint64_t stmts_count() { return stmts_.size(); }
    std::shared_ptr<Stmt> get_stmt(uint32_t index) {
        return index < stmts_.size() ? stmts_[index] : nullptr;
    }
    void remove_stmt(const std::shared_ptr<Stmt> &stmt);
    // helper function to initiate the blocks
    std::shared_ptr<SequentialStmtBlock> sequential();
    std::shared_ptr<CombinationalStmtBlock> combinational();

    // child generator. needed for generator merge
    void add_child_generator(const std::string &instance_name,
                             const std::shared_ptr<Generator> &child);
    void add_child_generator(const std::string &instance_name,
                             const std::shared_ptr<Generator> &child,
                             const std::pair<std::string, uint32_t> &debug_info);
    void remove_child_generator(const std::shared_ptr<Generator> &child);
    std::vector<std::shared_ptr<Generator>> get_child_generators();
    uint64_t inline get_child_generator_size() const { return children_.size(); }
    bool has_child_generator(const std::shared_ptr<Generator> &child);
    void accept_generator(IRVisitor *visitor) { visitor->visit(this); }

    void replace_child_generator(const std::shared_ptr<Generator> &target,
                                 const std::shared_ptr<Generator> &new_generator);

    // AST stuff
    void accept(IRVisitor *visitor) override;
    uint64_t inline child_count() override { return stmts_count() + get_child_generator_size(); }
    IRNode *get_child(uint64_t index) override;

    std::set<std::string> get_vars();

    std::set<std::string> get_all_var_names();

    std::string get_unique_variable_name(const std::string &prefix, const std::string &var_name);

    Context *context() const { return context_; }

    IRNode *parent() override { return parent_generator_; }

    bool is_stub() const { return is_stub_; }
    void set_is_stub(bool value) { is_stub_ = value; }

    // if imported from verilog or specified
    bool external() { return (!lib_files_.empty()) || is_external_; }
    std::string external_filename() const { return lib_files_.empty() ? "" : lib_files_[0]; }
    void set_external(bool value) { is_external_ = value; }

    std::shared_ptr<Stmt> wire_ports(std::shared_ptr<Port> &port1, std::shared_ptr<Port> &port2);

    bool debug = false;

    const std::unordered_set<std::shared_ptr<Generator>> &get_clones() const { return clones_; }
    std::shared_ptr<Generator> clone();
    bool is_cloned() const { return is_cloned_; }
    // this is for internal libraries only. use it only if you know what you're doing
    void set_is_cloned(bool value) { is_cloned_ = value; }

    // debug info
    const std::unordered_map<std::shared_ptr<Generator>, std::pair<std::string, uint32_t>>
        &children_debug() const {
        return children_debug_;
    }

    ~Generator() override = default;

private:
    std::vector<std::string> lib_files_;
    Context *context_;

    std::map<std::string, std::shared_ptr<Var>> vars_;
    std::set<std::string> ports_;
    std::map<std::string, std::shared_ptr<Param>> params_;
    std::unordered_set<std::shared_ptr<Expr>> exprs_;

    std::vector<std::shared_ptr<Stmt>> stmts_;

    std::unordered_map<std::string, std::shared_ptr<Generator>> children_;
    std::vector<std::string> child_names_;
    std::unordered_map<std::shared_ptr<Generator>, std::pair<std::string, uint32_t>>
        children_debug_;

    Generator *parent_generator_ = nullptr;

    std::unordered_set<std::shared_ptr<Const>> consts_;

    bool is_stub_ = false;
    bool is_external_ = false;

    // used for shallow cloning
    std::unordered_set<std::shared_ptr<Generator>> clones_;
    bool is_cloned_ = false;
};

}  // namespace kratos

#endif  // KRATOS_MODULE_HH22
