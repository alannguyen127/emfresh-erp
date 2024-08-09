frappe.ui.form.on("EFE Order", {
  refresh: function (frm) {
    // Setup trigger when 'Day Menu' field changes
    frm.fields_dict["efe_meal_box_selection"].grid.get_field(
      "day_menu"
    ).get_query = function (doc, cdt, cdn) {
      return {
        filters: {
          field_link: frm.doc.day_menu, // Ensure field_link matches the field linking Day Menu in EFE Meal Box
        },
      };
    };

    // Trigger to update Meal Box options based on selected Day Menu
    frm.fields_dict["efe_meal_box_selection"].grid
      .get_field("day_menu")
      .on("change", function () {
        let selected_day_menu = frm.doc.day_menu;
        if (selected_day_menu) {
          frappe.call({
            method: "frappe.client.get",
            args: {
              doctype: "EFE Day Menu",
              name: selected_day_menu,
            },
            callback: function (response) {
              if (response.message) {
                let meal_boxes = response.message.meal_box.map(
                  (mb) => mb.meal_box
                );
                frm.fields_dict["efe_meal_box_selection"].grid.get_field(
                  "meal_box"
                ).get_query = function () {
                  return {
                    filters: {
                      name: ["in", meal_boxes],
                    },
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
