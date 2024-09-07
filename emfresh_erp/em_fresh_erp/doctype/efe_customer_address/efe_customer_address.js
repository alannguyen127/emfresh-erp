// Copyright (c) 2024, Nghiem Nguyen and contributors
// For license information, please see license.txt

// frappe.ui.form.on("EFE Customer Address", {
// 	refresh(frm) {

// 	},
// });

// frappe.ui.form.on("EFE Customer Address", {

//   no_street: function (frm, cdt, cdn) {
//     sum_address(frm);
//   },
//   ward: function (frm, cdt, cdn) {
//     sum_address(frm);
//   },
//   district: function (frm, cdt, cdn) {
//     sum_address(frm);
//   },
// });

// function sum_address(frm) {
//   let address = "";
//   address =
//     frm.doc.no_street.trim() +
//       " ," +
//       frm.doc.ward.trim() +
//       " ," +
//       frm.doc.district.trim() || "";
//   frm.set_value("address", address);
// }

frappe.ui.form.on("EFE Customer Address", {
  no_street: function (frm, cdt, cdn) {
    sum_address(frm);
  },
  ward: function (frm, cdt, cdn) {
    sum_address(frm);
  },
  district: function (frm, cdt, cdn) {
    sum_address(frm);
  },
});

function sum_address(frm) {
  let address = frm.doc.no_street.trim() || "";

  // Lấy title của ward
  if (frm.doc.ward) {
    frappe.db.get_value("EFE Ward", frm.doc.ward, "title", (r) => {
      if (r && r.title) {
        address += ", " + r.title.trim();

        // Sau khi có title của ward, tiếp tục lấy title của district
        if (frm.doc.district) {
          frappe.db.get_value(
            "EFE District",
            frm.doc.district,
            "title",
            (r) => {
              if (r && r.title) {
                address += ", " + r.title.trim();
                frm.set_value("address", address);
              }
            }
          );
        } else {
          frm.set_value("address", address);
        }
      }
    });
  } else if (frm.doc.district) {
    // Nếu không có ward nhưng có district
    frappe.db.get_value("EFE District", frm.doc.district, "title", (r) => {
      if (r && r.title) {
        address += ", " + r.title.trim();
        frm.set_value("address", address);
      }
    });
  } else {
    // Nếu không có ward và district
    frm.set_value("address", address);
  }
}
