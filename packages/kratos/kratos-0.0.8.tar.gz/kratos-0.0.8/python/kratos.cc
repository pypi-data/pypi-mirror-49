#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include "../src/codegen.hh"
#include "../src/except.hh"
#include "../src/expr.hh"
#include "../src/generator.hh"
#include "../src/pass.hh"
#include "../src/stmt.hh"
#include "../src/util.hh"

#include "kratos_expr.hh"

namespace py = pybind11;
using std::shared_ptr;
using namespace kratos;

void init_pass(py::module &m);
void init_generator(py::module &m);
void init_expr(py::module &m);
void init_stmt(py::module &m);

// bind all the enums
void init_enum(py::module &m) {
    py::enum_<PortType>(m, "PortType")
        .value("Clock", PortType::Clock)
        .value("AsyncReset", PortType::AsyncReset)
        .value("ClockEnable", PortType::ClockEnable)
        .value("Data", PortType::Data)
        .value("Reset", PortType::Reset)
        .export_values();

    py::enum_<PortDirection>(m, "PortDirection")
        .value("In", PortDirection::In)
        .value("Out", PortDirection::Out)
        .value("InOut", PortDirection::InOut)
        .export_values();

    py::enum_<HashStrategy>(m, "HashStrategy")
        .value("SequentialHash", HashStrategy::SequentialHash)
        .value("ParallelHash", HashStrategy::ParallelHash)
        .export_values();

    py::enum_<StatementType>(m, "StatementType")
        .value("If", StatementType::If)
        .value("Switch", StatementType::Switch)
        .value("Assign", StatementType::Assign)
        .value("Block", StatementType::Block)
        .value("ModuleInstantiation", StatementType::ModuleInstantiation)
        .export_values();

    py::enum_<AssignmentType>(m, "AssignmentType")
        .value("Blocking", AssignmentType::Blocking)
        .value("NonBlocking", AssignmentType::NonBlocking)
        .value("Undefined", AssignmentType::Undefined)
        .export_values();

    py::enum_<StatementBlockType>(m, "StatementBlockType")
        .value("Combinational", StatementBlockType::Combinational)
        .value("Sequential", StatementBlockType::Sequential)
        .export_values();

    py::enum_<BlockEdgeType>(m, "BlockEdgeType")
        .value("Posedge", BlockEdgeType::Posedge)
        .value("Negedge", BlockEdgeType::Negedge)
        .export_values();

    py::enum_<IRNodeKind>(m, "IRNodeKind")
        .value("GeneratorKind", IRNodeKind::GeneratorKind)
        .value("VarKind", IRNodeKind::VarKind)
        .value("StmtKind", IRNodeKind::StmtKind)
        .export_values();

    py::enum_<VarCastType>(m, "VarCastType")
        .value("Signed", VarCastType::Signed)
        .value("AsyncReset", VarCastType::AsyncReset)
        .value("Clock", VarCastType::Clock);
}

// exception module
void init_except(py::module &m) {
    auto except_m = m.def_submodule("exception");
    py::register_exception<VarException>(except_m, "VarException");
    py::register_exception<StmtException>(except_m, "StmtException");
}

// util submodule
void init_util(py::module &m) {
    auto util_m = m.def_submodule("util");

    util_m
        .def("is_valid_verilog", py::overload_cast<const std::string &>(&is_valid_verilog),
             "Check if the verilog doesn't have any syntax errors. Notice that you "
             "have to have either verilator or iverilog in your $PATH to use this function")
        .def("is_valid_verilog",
             py::overload_cast<const std::map<std::string, std::string> &>(&is_valid_verilog),
             "Check if the verilog doesn't have any syntax errors. Notice that you "
             "have to have either verilator or iverilog in your $PATH to use this function");
}


void init_context(py::module &m) {
    auto context = py::class_<Context>(m, "Context");
    context.def(py::init())
        .def("generator", &Context::generator, py::return_value_policy::reference)
        .def("empty_generator", &Context::empty_generator)
        .def("clear", &Context::clear)
        .def("get_hash", &Context::get_hash)
        .def("get_generators_by_name", &Context::get_generators_by_name)
        .def("hash_table_size", &Context::hash_table_size)
        .def("change_generator_name", &Context::change_generator_name)
        .def("add", &Context::add)
        .def("has_hash", &Context::has_hash);
}


void init_code_gen(py::module &m) {
    py::class_<VerilogModule>(m, "VerilogModule")
        .def(py::init<Generator *>())
        .def("verilog_src", &VerilogModule::verilog_src)
        .def("run_passes", &VerilogModule::run_passes)
        .def("debug_info", &VerilogModule::debug_info)
        .def("pass_manager", &VerilogModule::pass_manager, py::return_value_policy::reference);
}

PYBIND11_MODULE(_kratos, m) {
    m.doc() = R"pbdoc(
        .. currentmodule:: _kratos
    )pbdoc";

    init_enum(m);
    init_pass(m);
    init_expr(m);
    init_context(m);
    init_generator(m);
    init_stmt(m);
    init_code_gen(m);
    init_util(m);
    init_except(m);
}
