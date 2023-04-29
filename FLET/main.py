from flet import *
import random
import datetime
import os


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
now = datetime.datetime.now()
formatted_date = now.strftime("%d-%m-%Y")


def main(page: Page):
    page.scroll = "auto"
    page.theme_mode = "light"

    all_food = Column()

    def addtofood(e):
        random_price = random.randint(500, 10000)
        total_price = random_price * int(con_input.content.controls[4].value)

        all_food.controls.append(
            Container(
                padding=10,
                bgcolor="yellow200",
                content=Column([
                    Text(con_input.content.controls[3].value,
                         weight="bold", size=20
                         ),
                    Text(f'total buy{con_input.content.controls[4].value}',
                         weight="bold", size=20
                         ),
                    Row([
                        Text("total price", weight="bold"),
                        Text(f"${'{:,.2f}'.format(total_price)}")
                    ], alignment="spaceBetween")
                ])
            )
        )
        page.update()

    con_input = Container(
        content=Column([
            TextField(label="username"),
            TextField(label="address"),
            Text("Input order food", size=25, weight="bold"),
            TextField(label="Food name"),
            TextField(label="You buy pcs"),
            ElevatedButton("add to food",
                           on_click=addtofood)
        ])
    )

    def savetomybilling(e: FilePickerResultEvent):
        you_file_save_location = e.path
        print(you_file_save_location)

        file_path = f"{you_file_save_location}.pdf"
        doc = SimpleDocTemplate(file_path, pagesizes=letter)

        elements = []

        styles = getSampleStyleSheet()

        elements.append(Paragraph("Billing order", styles['Title']))
        customer_name = con_input.content.controls[0].value

        elements.append(Paragraph(f'Name {customer_name}', styles['Normal']))

        elements.append(
            Paragraph(f"Date order {formatted_date}", styles['Normal']))

        address = con_input.content.controls[1].value

        elements.append(Paragraph(f'address: {address}', styles['Normal']))

        elements.append(
            Paragraph(f"You Order Food:", styles['Heading1']))

        list_order = []
        list_order.append(["Food name", "pcs", "price"])

        for b in all_food.controls:
            list_order.append([
                b.content.controls[0].value,
                b.content.controls[1].value.replace('$', '').replace(',', ''),
                b.content.controls[2].controls[1].value.replace(
                    '$', '').replace(',', ''),
            ])

        table = Table(list_order)

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 14),
            ("BOTTOM-PADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 0), (-1, -1), colors.beige),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 12),
            ("BOTTOM-PADDING", (0, 0), (-1, -1), 12),
        ]))

        elements.append(table)
        grand_total = sum([float(row[2]) for row in list_order[1:]])

        elements.append(
            Paragraph(f'grand total : ${grand_total: .2f}', styles['Heading1']))

        doc.build(elements)

        file_saver = FilePicker(
            on_result=savetomybilling
        )
        page.overlay.append(file_saver)

    def buildmyorder(e):
        mydialog = AlertDialog(
            title=Text("Billing order", size=30, weight="bold"),
            content=Column([
                Row([
                    Text(con_input.content.controls[0].value,
                         weight="bold", size=20),

                    Text(f"Order date : {formatted_date}",
                         weight="bold"),
                ]),
                Row([
                    Text("address", weight="bold"),
                    Text(con_input.content.controls[1].value,
                         weight="bold"),
                ], alignment="end"),
                Text("You Order Burger", weight="bold", size=25),
                all_food
            ], scroll="auto"),

            actions=[
                ElevatedButton("print my billing",
                               bgcolor="yellow", color="white",
                               on_click=lambda e:file_saver.save_file()
                               )
            ]
        )

        page.dialog = mydialog
        mydialog.open = True
        page.update()

    page.floating_action_button = FloatingActionButton(
        icon="add", bgcolor="yellow",
        on_click=buildmyorder
    )

    page.add(
        Column([
            con_input,
            Text("You Burger Order", weight="bold", size=20),
            all_food
        ])
    )


flet.app(target=main)
