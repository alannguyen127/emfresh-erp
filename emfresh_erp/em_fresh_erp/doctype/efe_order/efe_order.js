// frappe.ui.form.on("EFE Order", {
//   refresh: function (frm) {
//     frm.fields_dict["efe_meal_box_selection"].grid.get_field(
//       "day_menu"
//     ).get_query = function (doc, cdt, cdn) {
//       return {
//         filters: {
//           // Thêm bộ lọc nếu cần
//         },
//       };
//     };

//     // Khi chọn một ngày menu, cập nhật các tùy chọn cho món ăn
//     frm.fields_dict["efe_meal_box_selection"].grid
//       .get_field("day_menu")
//       .on("change", function () {
//         let selected_day_menu = frm.fields_dict["efe_meal_box_selection"].grid
//           .get_field("day_menu")
//           .get_value();

//         if (selected_day_menu) {
//           // Gọi đến server-side để lấy danh sách các món ăn của ngày menu đã chọn
//           frappe.call({
//             method: "frappe.client.get_list",
//             args: {
//               doctype: "EFE Day Menu",
//               filters: {
//                 name: selected_day_menu,
//               },
//               fields: ["meal_box"],
//             },
//             callback: function (r) {
//               if (r.message) {
//                 let meal_boxes = r.message.map((box) => box.meal_box);
//                 frm.fields_dict["efe_meal_box_selection"].grid.get_field(
//                   "meal_box"
//                 ).get_query = function () {
//                   return {
//                     filters: [["name", "in", meal_boxes]],
//                   };
//                 };
//                 frm.refresh_field("efe_meal_box_selection");
//               }
//             },
//           });
//         }
//       });
//   },
// });
frappe.ui.form.on("EFE Order", {
  onload: function (frm) {
    frm.fields_dict["efe_meal_box_selection"].grid.on("refresh", function () {
      if (
        frm.fields_dict["efe_meal_box_selection"] &&
        frm.fields_dict["efe_meal_box_selection"].grid
      ) {
        frm.fields_dict["efe_meal_box_selection"].grid.get_field(
          "day_menu"
        ).get_query = function (doc, cdt, cdn) {
          return {
            filters: {
              // Thêm bộ lọc nếu cần
            },
          };
        };
      }
    });

    frm.fields_dict["efe_meal_box_selection"].grid
      .get_field("day_menu")
      .on("change", function () {
        let selected_day_menu = frm.fields_dict["efe_meal_box_selection"].grid
          .get_field("day_menu")
          .get_value();

        if (selected_day_menu) {
          frappe.call({
            method: "your_custom_app.path.to.get_meal_boxes",
            args: {
              day_menu: selected_day_menu,
            },
            callback: function (r) {
              if (r.message) {
                let meal_boxes = r.message;
                frm.fields_dict["efe_meal_box_selection"].grid.get_field(
                  "meal_box"
                ).get_query = function () {
                  return {
                    filters: [["name", "in", meal_boxes]],
                  };
                };
                frm.refresh_field("efe_meal_box_selection");
              }
            },
          });
        }
      });
  },
});
