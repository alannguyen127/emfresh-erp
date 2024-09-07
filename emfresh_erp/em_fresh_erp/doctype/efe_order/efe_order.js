frappe.ui.form.on("EFE Order", {
  // refresh: function (frm) {
  //   // Tính tổng số tiền khi form được làm mới
  //   calculate_total_amount(frm);
  // },

  onload: function (frm) {
    calculate_total_amount(frm);
  },
  shipping_fee: function (frm, cdt, cdn) {
    calculate_total_amount(frm);
  },
});

frappe.ui.form.on("EFE Order Meal Package", {
  // Triggered when a field changes

  total_price: function (frm, cdt, cdn) {
    calculate_total_amount(frm);
  },
  order_meal_package_remove: function (frm, cdt, cdn) {
    // alert('remove item for add ons');
    // frappe.msgprint('remove item for add ons');
    calculate_total_amount(frm);
  },
});
frappe.ui.form.on("EFE Order Extra Item", {
  // Triggered when a field changes
  total_price: function (frm, cdt, cdn) {
    calculate_total_amount(frm);
  },
});

// Hàm tính tổng số tiền từ các bảng con
function calculate_total_amount(frm) {
  let total_amount = 0;

  // Tổng giá trị trong bảng con Order Meal Package
  frm.doc.order_meal_package.forEach(function (row) {
    total_amount += row.total_price || 0; // Đảm bảo giá trị tồn tại, nếu không thì là 0
  });

  // Tổng giá trị trong bảng con Order Extra Item
  frm.doc.order_extra_item.forEach(function (row) {
    total_amount += row.total_price || 0; // Đảm bảo giá trị tồn tại, nếu không thì là 0
  });

  total_amount += frm.doc.shipping_fee || 0;
  // Cập nhật trường Total Amount với tổng số tiền đã tính
  frm.set_value("total_amount", total_amount);
}

// function calculate_total_price(frm) {
//   let total_price = 0;

//   frm.doc.order_meal_package.forEach(function (row) {
//     total_price = unit_price * quantity;
//   });

//   frm.set_value("total_price", total_price);
// }

frappe.ui.form.on("EFE Order Meal Package", {
  // Triggered when a field changes

  quantity: function (frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    if (row.unit_price) {
      let total_price = row.unit_price * row.quantity;
      frappe.model.set_value(cdt, cdn, "total_price", total_price);
    }
  },
  unit_price: function (frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    if (row.quantity) {
      let total_price = row.unit_price * row.quantity;
      frappe.model.set_value(cdt, cdn, "total_price", total_price);
    }
  },

  meal_package: function (frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    let quantity = row.quantity;
    quantity = 0;
    frappe.model.set_value(cdt, cdn, "quantity", quantity);
  },
});

// function cal_total(price, qty) {
//   if (price && qty) {
//     return price * qty;
//   }
//   return 0;
// }
frappe.ui.form.on("EFE Order Extra Item", {
  // Triggered when a field changes

  quantity: function (frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    if (row.unit_price) {
      let total_price = row.unit_price * row.quantity;
      frappe.model.set_value(cdt, cdn, "total_price", total_price);
    }
  },
  unit_price: function (frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    if (row.quantity) {
      let total_price = row.unit_price * row.quantity;
      frappe.model.set_value(cdt, cdn, "total_price", total_price);
    }
  },

  extra: function (frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    let quantity = row.quantity;
    quantity = 0;
    frappe.model.set_value(cdt, cdn, "quantity", quantity);
  },
});
