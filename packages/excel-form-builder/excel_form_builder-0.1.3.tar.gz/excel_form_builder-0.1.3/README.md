# excel_form_builder
Converts xlsx files to json mobile forms to be used in Device Magic.

## Installation
```python
pip install excel-form-builder
```

## Creating the JSON
Within the bin directory, in terminal execute:
```python
python3 create_form path/to/xlsx
Form created! # JSON is placed in same directory as the Excel file
```

## Excel File Structure

Each row represents a question or group, blank rows are ignored.

Input the question type in the first cell and then place the question name in the cell to the right.

![alt text](screenshots/type&name.png "type&name")

Place a question's hint to the right of the name and prefix the text with a colon. Ex. :hint

For select questions, place each select option in separate cells to the right of the name and hint (if it exists).

When a group is added to a form, the questions inside the group will need to be indented one cell to the right.  Ex. A subform with the type defined in column A will require it's questions to have their type defined in column B in the rows that follow.

![alt text](screenshots/group.png "group")

After all necessary questions are added to the group, simply start the next question one column to the left of the previous row's question.

For more information, see the [example directory](https://github.com/aseli1/dm_excel_form_builder/blob/master/example/Sample.xlsx).
