// Copyright (c) 2024, Nghiem Nguyen and contributors
// For license information, please see license.txt

// frappe.ui.form.on("EFE Week Menu", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("EFE Week Menu", {
  refresh: function (frm) {
    frappe.call({
      method: "frappe.client.get_list",
      args: {
        doctype: "EFE Day Menu",
        filters: {
          week_menu: frm.doc.name,
        },
        fields: ["name", "date"],
      },
      callback: function (r) {
        if (r.message) {
          // r.message.sort(function (a, b) {
          //   return new Date(a.date) - new Date(b.date);
          // });
          console.log("Sorted:", r.message);
          let html = "";
          let promises = [];

          r.message.forEach(function (d) {
            promises.push(
              frappe.call({
                method: "frappe.client.get",
                args: {
                  doctype: "EFE Day Menu",
                  name: d.name,
                },
                callback: function (res) {
                  if (res.message) {
                    // Kiểm tra xem meal_box có tồn tại không
                    let meal_boxes =
                      res.message.meal_box && res.message.meal_box.length > 0
                        ? res.message.meal_box
                            .map((box) => box.meal_box_title || "Unknown") // Lấy tên hoặc 'Unknown' nếu không có tên
                            .join(", ")
                        : "No meal boxes";

                    html += `<p><strong>Date:</strong> ${d.date} | <strong>Meal Boxes:</strong> ${meal_boxes}`;
                    //<a href="/app/efe-day-menu/${d.name}">${d.name}</a></p>//;
                  }
                },
              })
            );
          });

          Promise.all(promises).then(() => {
            frm.fields_dict.efe_day_menu_html.$wrapper.html(html);
          });
        }
      },
    });
  },
});
