/**
Copyright (c) 2016-2019 cloudover.io ltd.

Licensee holding a valid commercial license for dinemic library may use it with
accordance to terms of the license agreement between cloudover.io ltd. and the
licensee, or on GNU Affero GPL v3 license terms.

Licensee not holding a valid commercial license for dinemic library may use it
under GNU Affero GPL v3 license.

Terms of GNU Affero GPL v3 license are available on following site:
https://www.gnu.org/licenses/agpl-3.0.en.html
*/

#include "module.h"

using namespace boost::python;
using namespace std;

Dinemic::Sync::SyncInterface *py_sync = NULL;
Dinemic::Store::StoreInterface *py_store = NULL;

void launch() {
    py_store = new Dinemic::Store::RedisDriver();
    py_sync = new Dinemic::Sync::ZeroMQSync(py_store);
    py_sync->start_agent();
}

void shutdown() {
    py_sync->stop_agent();
}

void dinemic_exception_to_py(Dinemic::DException const &x) {
    PyErr_SetString(PyExc_Exception, x.get_reason().c_str());
}

void set_loglevel(string loglevel) {
    if (loglevel == "verbose")
        Dinemic::set_loglevel(Dinemic::loglevel_verbose);
    else if (loglevel == "debug")
        Dinemic::set_loglevel(Dinemic::loglevel_debug);
    else if (loglevel == "info")
        Dinemic::set_loglevel(Dinemic::loglevel_info);
    else if (loglevel == "error")
        Dinemic::set_loglevel(Dinemic::loglevel_error);
    else if (loglevel == "action")
        Dinemic::set_loglevel(Dinemic::loglevel_action);
    else if (loglevel == "none")
        Dinemic::set_loglevel(Dinemic::loglevel_none);
    else
        throw Dinemic::DException("Unknown loglevel");
}

namespace boost {
    namespace python {
        template <>
        struct has_back_reference<PyDModel>
          : boost::mpl::true_
        {};
        template <>
        struct has_back_reference<PyDField>
          : boost::mpl::true_
        {};
    }
}

BOOST_PYTHON_MODULE(pydinemic) {

    def("launch", &launch);
    def("shutdown", &launch);
    def("set_loglevel", &set_loglevel);
    register_exception_translator<Dinemic::DException>(dinemic_exception_to_py);

    class_ <PyDModel>("DModel", init<string, boost::python::list>(args("model_name", "authorized_object_ids"), "Create new object in Dinemic database with authorized objects"))
            .def(init<string, string>(args("db_id", "caller_id"), "Recreate existing in Dinemic database object, from given full dabtabase id"))
            .def("get_id", &PyDModel::get_id)
            .def("get_db_id", &PyDModel::get_db_id)
            .def("get_model", &PyDModel::get_model)
            .def("object_list_owned", &PyDModel::object_list_owned)
            .def("object_list", &PyDModel::object_list)
            .def("set", &PyDModel::set)
            .def("get", &PyDModel::get)
            .def("del", &PyDModel::del)
            .def("add_field", &PyDModel::map_fields);
    class_<PyAction>("DAction", init<>())
          .def("apply", &PyAction::py_apply)
          .def("revoke", &PyAction::py_revoke)
          .def("set_on_create_callback", &PyAction::set_callback_on_create)
          .def("set_on_created_callback", &PyAction::set_callback_on_created)
          .def("set_on_owned_created_callback", &PyAction::set_callback_on_owned_created)
          .def("set_on_update_callback", &PyAction::set_callback_on_update)
          .def("set_on_authorized_update_callback", &PyAction::set_callback_on_authorized_update)
          .def("set_on_owned_update_callback", &PyAction::set_callback_on_owned_update)
          .def("set_on_updated_callback", &PyAction::set_callback_on_updated)
          .def("set_on_authorized_updated_callback", &PyAction::set_callback_on_authorized_updated)
          .def("set_on_owned_updated_callback", &PyAction::set_callback_on_owned_updated);
    class_<PyDField>("DField", init<string, bool>(args("field_name", "is_encrypted")))
          .def("set", &PyDField::set)
          .def("get", &PyDField::get);
}
