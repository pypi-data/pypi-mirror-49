#include "expr.hh"
#include <iostream>
#include <stdexcept>
#include "except.hh"
#include "fmt/format.h"
#include "generator.hh"
#include "stmt.hh"
#include "util.hh"

using fmt::format;
using std::make_shared;
using std::runtime_error;
using std::shared_ptr;
using std::string;
using std::vector;

namespace kratos {

bool is_relational_op(ExprOp op) {
    static std::unordered_set<ExprOp> ops = {ExprOp::LessThan, ExprOp::GreaterThan,
                                             ExprOp::LessEqThan, ExprOp::GreaterEqThan, ExprOp::Eq};
    return ops.find(op) != ops.end();
}

std::pair<std::shared_ptr<Var>, std::shared_ptr<Var>> Var::get_binary_var_ptr(
    const Var &var) const {
    auto left = const_cast<Var *>(this)->shared_from_this();
    auto right = const_cast<Var *>(&var)->shared_from_this();
    return {left, right};
}

Expr &Var::operator-(const Var &var) const {
    const auto &[left, right] = get_binary_var_ptr(var);
    return generator->expr(ExprOp::Minus, left, right);
}

Expr &Var::operator-() const {
    auto var = generator->get_var(name);
    return generator->expr(ExprOp::Minus, var, nullptr);
}

Expr &Var::operator~() const {
    auto var = generator->get_var(name);
    return generator->expr(ExprOp::UInvert, var, nullptr);
}

Expr &Var::operator+() const {
    auto var = generator->get_var(name);
    return generator->expr(ExprOp::UPlus, var, nullptr);
}

Expr &Var::operator+(const Var &var) const {
    const auto &[left, right] = get_binary_var_ptr(var);
    return generator->expr(ExprOp::Add, left, right);
}

Expr &Var::operator*(const Var &var) const {
    const auto &[left, right] = get_binary_var_ptr(var);
    return generator->expr(ExprOp::Multiply, left, right);
}

Expr &Var::operator%(const Var &var) const {
    const auto &[left, right] = get_binary_var_ptr(var);
    return generator->expr(ExprOp::Mod, left, right);
}

Expr &Var::operator/(const Var &var) const {
    const auto &[left, right] = get_binary_var_ptr(var);
    return generator->expr(ExprOp::Divide, left, right);
}

Expr &Var::operator>>(const Var &var) const {
    const auto &[left, right] = get_binary_var_ptr(var);
    return generator->expr(ExprOp::LogicalShiftRight, left, right);
}

Expr &Var::operator<<(const Var &var) const {
    const auto &[left, right] = get_binary_var_ptr(var);
    return generator->expr(ExprOp::ShiftLeft, left, right);
}

Expr &Var::operator|(const Var &var) const {
    const auto &[left, right] = get_binary_var_ptr(var);
    return generator->expr(ExprOp::Or, left, right);
}

Expr &Var::operator&(const Var &var) const {
    const auto &[left, right] = get_binary_var_ptr(var);
    return generator->expr(ExprOp::And, left, right);
}

Expr &Var::operator^(const Var &var) const {
    const auto &[left, right] = get_binary_var_ptr(var);
    return generator->expr(ExprOp::Xor, left, right);
}

Expr &Var::ashr(const Var &var) const {
    const auto &[left, right] = get_binary_var_ptr(var);
    return generator->expr(ExprOp::SignedShiftRight, left, right);
}

Expr &Var::operator<(const Var &var) const {
    const auto &[left, right] = get_binary_var_ptr(var);
    return generator->expr(ExprOp::LessThan, left, right);
}

Expr &Var::operator>(const Var &var) const {
    const auto &[left, right] = get_binary_var_ptr(var);
    return generator->expr(ExprOp::GreaterThan, left, right);
}

Expr &Var::operator<=(const Var &var) const {
    const auto &[left, right] = get_binary_var_ptr(var);
    return generator->expr(ExprOp::LessEqThan, left, right);
}

Expr &Var::operator>=(const Var &var) const {
    const auto &[left, right] = get_binary_var_ptr(var);
    return generator->expr(ExprOp::GreaterEqThan, left, right);
}

Expr &Var::eq(const Var &var) const {
    const auto &[left, right] = get_binary_var_ptr(var);
    return generator->expr(ExprOp::Eq, left, right);
}

Expr &Var::operator!=(const Var &var) const {
    const auto &[left, right] = get_binary_var_ptr(var);
    return generator->expr(ExprOp::Neq, left, right);
}

VarSlice &Var::operator[](std::pair<uint32_t, uint32_t> slice) {
    auto const [high, low] = slice;
    if (low > high) {
        throw VarException(::format("low ({0}) cannot be larger than ({1})", low, high), {this});
    }
    if (high >= width) {
        throw VarException(::format("high ({0}) has to be smaller than width ({1})", high, width),
                           {this});
    }
    // if we already has the slice
    if (slices_.find(slice) != slices_.end()) return *slices_.at(slice);
    // create a new one
    // notice that slice is not part of generator's variables. It's handled by the parent (var)
    // itself
    auto var_slice = ::make_shared<VarSlice>(this, high, low);
    slices_.emplace(slice, var_slice);
    return *slices_.at(slice);
}

VarConcat &Var::concat(Var &var) {
    auto ptr = var.shared_from_this();
    // notice that we effectively created an implicit sink->sink by creating a concat
    // however, it's not an assignment, that's why we need to use concat_vars to hold the
    // vars
    for (auto const &exist_var : concat_vars_) {
        // reuse the existing variables
        if (exist_var->vars().size() == 2 && exist_var->vars().back() == ptr) {
            return *exist_var;
        }
    }
    auto concat_ptr = std::make_shared<VarConcat>(generator, shared_from_this(), ptr);
    concat_vars_.emplace(concat_ptr);
    return *concat_ptr;
}

std::string Var::to_string() const { return name; }

VarSlice &Var::operator[](uint32_t bit) { return (*this)[{bit, bit}]; }

VarSlice::VarSlice(Var *parent, uint32_t high, uint32_t low)
    : Var(parent->generator, "", high - low + 1, parent->is_signed, VarType::Slice),
      parent_var(parent),
      low(low),
      high(high) {}

std::string VarSlice::get_slice_name(const std::string &parent_name, uint32_t high, uint32_t low) {
    return ::format("{0}[{1}:{2}]", parent_name, high, low);
}

std::string VarSlice::to_string() const {
    return get_slice_name(parent_var->to_string(), high, low);
}

Expr::Expr(ExprOp op, const ::shared_ptr<Var> &left, const ::shared_ptr<Var> &right)
    : Var(left->generator, "", left->width, left->is_signed), op(op), left(left), right(right) {
    if (left == nullptr) throw std::runtime_error("left operand is null");
    generator = left->generator;
    if (right != nullptr && left->width != right->width)
        throw VarException(
            ::format("left ({0}) width ({1}) doesn't match with right ({2}) width ({3})",
                     left->to_string(), left->width, right->to_string(), right->width),
            {left.get(), right.get()});
    // if it's a predicate/relational op, the width is one
    if (is_relational_op(op))
        width = 1;
    else
        width = left->width;

    name = to_string();
    if (right != nullptr)
        is_signed = left->is_signed & right->is_signed;
    else
        is_signed = left->is_signed;
    type_ = VarType::Expression;
}

Var::Var(Generator *module, const std::string &name, uint32_t width, bool is_signed)
    : Var(module, name, width, is_signed, VarType::Base) {}

Var::Var(Generator *module, const std::string &name, uint32_t width, bool is_signed, VarType type)
    : IRNode(IRNodeKind::VarKind),
      name(name),
      width(width),
      is_signed(is_signed),
      generator(module),
      type_(type) {
    if (module == nullptr) throw ::runtime_error(::format("module is null for {0}", name));
}

IRNode *Var::parent() { return generator; }
IRNode *VarSlice::parent() { return parent_var; }

std::shared_ptr<AssignStmt> Var::assign(const std::shared_ptr<Var> &var) {
    return assign(var, AssignmentType::Undefined);
}

std::shared_ptr<AssignStmt> Var::assign(Var &var) {
    return assign(var.shared_from_this(), AssignmentType::Undefined);
}

std::shared_ptr<AssignStmt> Var::assign(const std::shared_ptr<Var> &var, AssignmentType type) {
    // if it's a constant or expression, it can't be assigned to
    if (type_ == VarType::ConstValue)
        throw VarException(::format("Cannot assign {0} to a const {1}", var->to_string(), name),
                           {this, var.get()});
    else if (type_ == VarType::Expression)
        throw VarException(::format("Cannot assign {0} to an expression", var->to_string(), name),
                           {this, var.get()});
    auto const &stmt = ::make_shared<AssignStmt>(shared_from_this(), var, type);

    return stmt;
}

void Var::unassign(const std::shared_ptr<AssignStmt> &stmt) {
    // we need to take care of the slices
    stmt->right()->sinks_.erase(stmt);
    sources_.erase(stmt);
    // erase from parent if any
    // TODO: fix this will proper parent
    generator->remove_stmt(stmt);
}

Const::Const(Generator *generator, int64_t value, uint32_t width, bool is_signed)
    : Var(generator, std::to_string(value), width, is_signed, VarType::ConstValue), value_() {
    // need to deal with the signed value
    if (is_signed) {
        // compute the -max value
        uint64_t temp = (~0ull) << (width - 1);
        int64_t min = 0;
        std::memcpy(&min, &temp, sizeof(min));
        if (value < min)
            throw ::runtime_error(::format(
                "{0} is smaller than the minimum value ({1}) given width {2}", value, min, width));
        temp = (1ull << (width - 1)) - 1;
        int64_t max;
        std::memcpy(&max, &temp, sizeof(max));
        if (value > max)
            throw ::runtime_error(::format(
                "{0} is larger than the maximum value ({1}) given width {2}", value, max, width));
    } else {
        uint64_t max = (1ull << width) - 1;
        uint64_t unsigned_value;
        std::memcpy(&unsigned_value, &value, sizeof(unsigned_value));
        if (unsigned_value > max)
            throw ::runtime_error(::format(
                "{0} is larger than the maximum value ({1}) given width {2}", value, max, width));
    }
    value_ = value;
}

VarCasted::VarCasted(Var *parent, VarCastType cast_type)
    : Var(parent->generator, "", parent->width, true, parent->type()),
      parent_var_(parent),
      cast_type_(cast_type) {
    type_ = VarType::BaseCasted;
    if (cast_type_ == Signed) is_signed = true;
}

std::shared_ptr<AssignStmt> VarCasted::assign(const std::shared_ptr<Var> &, AssignmentType) {
    throw VarException(::format("{0} is not allowed to be a sink", to_string()), {this});
}

std::string VarCasted::to_string() const {
    if (cast_type_ == VarCastType::Signed)
        return ::format("$signed({0})", parent_var_->to_string());
    else
        return parent_var_->to_string();
}

void VarCasted::add_sink(const std::shared_ptr<AssignStmt> &stmt) { parent_var_->add_sink(stmt); }

std::shared_ptr<Var> Var::cast(VarCastType cast_type) {
    if (cast_type == VarCastType::Signed && is_signed) {
        return shared_from_this();
    } else if (casted_.find(cast_type) != casted_.end()) {
        return casted_.at(cast_type);
    } else {
        casted_.emplace(cast_type, std::make_shared<VarCasted>(this, cast_type));
        return casted_.at(cast_type);
    }
}

void Const::set_value(int64_t new_value) {
    try {
        Const c(generator, new_value, width, is_signed);
        value_ = new_value;
    } catch (::runtime_error &) {
        std::cerr << ::format("Unable to set value from {0} to {1}", value_, new_value)
                  << std::endl;
    }
}

void Const::add_source(const std::shared_ptr<AssignStmt> &) {
    throw VarException(::format("const {0} is not allowed to be driven by a net", to_string()),
                       {this});
}

Param::Param(Generator *m, std::string name, uint32_t width, bool is_signed)
    : Const(m, 0, width, is_signed), parameter_name_(std::move(name)) {
    // override the type value
    type_ = VarType::Parameter;
}

VarConcat::VarConcat(Generator *m, const std::shared_ptr<Var> &first,
                     const std::shared_ptr<Var> &second)
    : Var(m, "", first->width + second->width, first->is_signed && second->is_signed,
          VarType::Expression) {
    if (first->is_signed != second->is_signed)
        throw VarException(
            ::format("{0} is signed but {1} is not", first->to_string(), second->to_string()),
            {first.get(), second.get()});
    vars_.emplace_back(first);
    vars_.emplace_back(second);
}

void VarConcat::add_source(const std::shared_ptr<kratos::AssignStmt> &stmt) {
    for (auto &var : vars_) {
        var->add_source(stmt);
    }
}

void VarConcat::add_sink(const std::shared_ptr<kratos::AssignStmt> &stmt) {
    for (auto &var : vars_) {
        var->add_sink(stmt);
    }
}

std::string VarConcat::to_string() const {
    std::vector<std::string> var_names;
    for (const auto &ptr : vars_) {
        var_names.emplace_back(ptr->to_string());
    }
    auto content = fmt::join(var_names.begin(), var_names.end(), ", ");
    return ::format("{{{0}}}", content);
}

VarConcat::VarConcat(VarConcat *first, const std::shared_ptr<Var> &second)
    : Var(first->generator, "", first->width + second->width, first->is_signed && second->is_signed,
          VarType::Expression) {
    if (first->is_signed != second->is_signed)
        throw VarException(
            ::format("{0} is signed but {1} is not", first->to_string(), second->to_string()),
            {first, second.get()});
    vars_ = std::vector<std::shared_ptr<Var>>(first->vars_.begin(), first->vars_.end());
    vars_.emplace_back(second);
}

VarConcat& VarConcat::concat(kratos::Var &var) {
    auto result = std::make_shared<VarConcat>(this, var.shared_from_this());
    // add it to the first one
    vars_[0]->add_concat_var(result);
    return *result;
}

std::string Const::to_string() const {
    if (is_signed && value_ < 0) {
        return ::format("-{0}\'h{1:X}", width, -value_);
    } else {
        return ::format("{0}\'h{1:X}", width, value_);
    }
}

std::shared_ptr<AssignStmt> Var::assign(Var &var, AssignmentType type) {
    // need to find the pointer
    auto var_ptr = var.shared_from_this();
    return assign(var_ptr, type);
}

std::string inline expr_to_string(const Expr *expr, bool is_top) {
    auto left = expr->left;
    auto right = expr->right;

    auto left_str = left->type() == VarType::Expression
                        ? expr_to_string(left->as<Expr>().get(), expr->op == left->as<Expr>()->op)
                        : left->to_string();

    if (right != nullptr) {
        auto right_str =
            right->type() == VarType::Expression
                ? expr_to_string(right->as<Expr>().get(), expr->op == right->as<Expr>()->op)
                : right->to_string();
        if (is_top)
            return ::format("{0} {1} {2}", left_str, ExprOpStr(expr->op), right_str);
        else
            return ::format("({0} {1} {2})", left_str, ExprOpStr(expr->op), right_str);
    } else {
        if (is_top)
            return ::format("{0}{1}", ExprOpStr(expr->op), left_str);
        else
            return ::format("({0}{1})", ExprOpStr(expr->op), left_str);
    }
}

std::string Expr::to_string() const { return expr_to_string(this, true); }

IRNode *Expr::get_child(uint64_t index) {
    if (index == 0)
        return left.get();
    else if (index == 1)
        return right ? right.get() : nullptr;
    else
        return nullptr;
}

void change_var_expr(std::shared_ptr<Expr> expr, Var *target, Var *new_var) {
    if (expr->left->type() == VarType::Expression) {
        expr = expr->left->as<Expr>();
        change_var_expr(expr, target, new_var);
    } else if (expr->right && expr->right->type() == VarType::Expression) {
        expr = expr->right->as<Expr>();
        change_var_expr(expr, target, new_var);
    } else {
        if (expr->left.get() == target) expr->left = new_var->shared_from_this();
        if (expr->right && expr->right.get() == target) expr->right = new_var->shared_from_this();
    }
}

void stmt_set_right(AssignStmt *stmt, Var *target, Var *new_var) {
    auto right = stmt->right();
    if (right->type() == VarType::Base || right->type() == VarType::PortIO ||
        right->type() == VarType::ConstValue) {
        if (right.get() == target)
            stmt->set_right(new_var->shared_from_this());
        else
            throw ::runtime_error("target not found");
    } else if (right->type() == VarType::Slice) {
        auto slice = right->as<VarSlice>();
        if (slice->parent_var != target) throw ::runtime_error("target not found");
        slice->set_parent(new_var);
    } else if (right->type() == VarType::Expression) {
        change_var_expr(stmt->right()->as<Expr>(), target, new_var);
    }
}

void Var::move_src_to(Var *var, Var *new_var, Generator *parent, bool keep_connection) {
    // only base and port vars are allowed
    if (var->type_ == VarType::Expression || var->type_ == VarType::ConstValue)
        throw ::runtime_error("Only base or port variables are allowed.");

    for (auto &stmt : var->sources_) {
        stmt->set_left(new_var->shared_from_this());
        if (parent->debug) {
            stmt->fn_name_ln.emplace_back(std::make_pair(__FILE__, __LINE__));
        }
        new_var->sources_.emplace(stmt);
    }
    // now clear the sources
    var->sources_.clear();

    if (keep_connection) {
        // create an assignment and add it to the parent
        auto stmt = var->assign(new_var->shared_from_this());
        if (parent->debug) {
            stmt->fn_name_ln.emplace_back(std::make_pair(__FILE__, __LINE__));
        }
        parent->add_stmt(stmt);
    }
}

void Var::move_sink_to(Var *var, Var *new_var, Generator *parent, bool keep_connection) {
    // only base and port vars are allowed
    if (var->type_ == VarType::Expression || var->type_ == VarType::ConstValue)
        throw ::runtime_error("Only base or port variables are allowed.");

    for (auto &stmt : var->sinks_) {
        stmt_set_right(stmt.get(), var, new_var);
        if (parent->debug) {
            stmt->fn_name_ln.emplace_back(std::make_pair(__FILE__, __LINE__));
        }
        new_var->sinks_.emplace(stmt);
    }
    // now clear the sinks
    var->sinks_.clear();

    if (keep_connection) {
        // create an assignment and add it to the parent
        auto stmt = new_var->assign(var->shared_from_this());
        if (parent->debug) {
            stmt->fn_name_ln.emplace_back(std::make_pair(__FILE__, __LINE__));
        }
        parent->add_stmt(stmt);
    }
}

void Expr::add_sink(const std::shared_ptr<AssignStmt> &stmt) {
    left->add_sink(stmt);
    if (right) right->add_sink(stmt);
}

void VarSlice::add_sink(const std::shared_ptr<AssignStmt> &stmt) {
    Var *parent = parent_var;
    while (parent->type() == VarType::Slice) {
        auto ptr = reinterpret_cast<VarSlice *>(parent);
        parent = ptr->parent_var;
    }
    parent->add_sink(stmt);
}

void VarSlice::add_source(const std::shared_ptr<AssignStmt> &stmt) {
    Var *parent = parent_var;
    while (parent->type() == VarType::Slice) {
        auto ptr = reinterpret_cast<VarSlice *>(parent);
        parent = ptr->parent_var;
    }
    parent->add_source(stmt);
}

Array::Array(kratos::Generator *m, const std::string &name, uint32_t width, uint32_t size,
             bool is_signed)
    : Var(m, name, width * size, is_signed), size_(size) {}

VarSlice &Array::operator[](uint32_t index) {
    if (index * size_ > width) throw VarException("index out of range", {});
    auto slice = std::make_shared<ArraySlice>(this, (index + 1) * size_ - 1, index * size_);
    slices_.emplace(std::make_pair(slice->high, slice->low), slice);
    return *slice;
}

VarSlice &Array::operator[](std::pair<uint32_t, uint32_t>) {
    throw std::runtime_error("Not implemented");
}

std::string ArraySlice::to_string() const {
    auto p = dynamic_cast<Array *>(parent_var);
    uint32_t index = low / p->size();
    uint32_t index_1 = (high + 1) / p->size();
    if (index_1 != index + 1) {
        throw VarException("Internal error on array slice.", {this});
    }
    return ::format("{0}[{1}]", p->name, index);
}

}