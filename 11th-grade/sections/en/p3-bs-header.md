<!-- page 156 -->

> **Workshop (continued)**
>
> Complete the content of the paragraph elements based on the image below. Use the right tag to show words in bold (bold). Save the file and check the result in the browser.
>
> ![Book image](../images/p162-01.png)
>
> To fix the mobile view, remove the w-75 class from the article element and add its style to the file `styles.css`:
>
> ![Book image](../images/p162-02.png)
>
> For devices narrower than 600 pixels, add the rule below to the file `styles.css`:
>
> ![Book image](../images/p162-03.png)

> **Learn more**
>
> **Designing a toolbar with a logo, a search box, the login | sign-up option, and a shopping cart**
>
> In this workshop you will create an area like the image below above the menu bar:
>
> ![Book image](../images/p162-04.png)
>
> Create a logo 70 pixels high and save the image as `logo.jpg` in the site's images folder.
>
> A search icon must appear inside the search box. To download a search icon, go to `svgrepo.com` and search for search. Use the Edit vector button to set your chosen icon to the smallest size and a color you like, then click Export. Save the icon file as `search.svg` in the site's images folder (images).

<!-- page 157 -->

> **Learn more (continued)**
>
> The image on the previous page has a logo, a search box (with a search icon and a text box), the login | sign-up option, and a shopping cart. Add these elements to the page `index.html` before the nav element, as below:
>
> ![Book image](../images/p163-01.png)
>
> Set the style of the elements in the desktop view as below:
>
> ![Book image](../images/p163-02.png)
>
> Add the classes below to the toolbar element. Then save the file and check the result in the browser.
>
> ![Book image](../images/p163-03.png)

<!-- page 158 -->

> **Learn more (continued)**
>
> With the CSS settings above, the «**Login|Sign up**» option and the **logo** are removed from the mobile view, so these options must be shown somewhere else. It is best to show them as a fixed bar at the bottom of the page. For this, enter the code below before `</main>`:
>
> ![Book image](../images/p164-01.png)
>
> The fixed-bottom class keeps the bottom-toolbar bar fixed at the bottom of the page.
>
> Write the style below for the bottom-toolbar element:
>
> ![Book image](../images/p164-02.png)
>
> Add the style below so the toolbar shows correctly in the mobile view:
>
> ![Book image](../images/p164-03.png)
>
> With these settings, the bottom-toolbar element appears at the bottom of the phone screen as in the figure below.
>
> ![Book image](../images/p164-04.png)
>
> To put some space between the menu and the toolbar, use the mt-3 class in the `<nav>` tag.
>
> Since the **Login|Sign up** and **shopping cart** options have been added to the toolbar, remove the user-actions element from the navigation menu (the top-menu element). Then remove its styles from the file `styles.css`. With the user-action area gone, the `.top-menu` class no longer needs the flex properties, so remove them too. In the end, only the max-width property remains in the top-menu class.
>
> ![Book image](../images/p164-05.png)

<!-- page 159 -->

> **Learn more (continued)**
>
> It is better to spread the menu options horizontally across the middle of the page; for this, use the `justify-content-center` class on the ul element:
>
> ![Book image](../images/p165-01.png)
>
> With the code above, all the properties of the selector `.top-menu ul` are replaced with the equivalent Bootstrap classes. So remove the properties inside the selector `.top-menu ul` from the file `styles.css`.
>
> With the settings above you should get the result below:
>
> ![Book image](../images/p165-02.png)

### Customizing Bootstrap classes

Bootstrap classes have predefined properties and values that make it quick to design page elements. Sometimes the developer needs to change how these classes behave. This can be done with CSS and SASS¹. To change the style of a class with CSS, set the class's property to the new values. By default the Bootstrap class has higher priority, so to give the custom class more weight you must put `!important` at the end of the new value; otherwise the new value is not applied.

> **Workshop**
>
> **Changing the style of a Bootstrap color class**
>
> In this workshop you will change the color of the bg-light class in the file `index.html`. For this, write the style below for the bg-light class:
>
> ![Book image](../images/p165-03.png)
>
> The file `styles.css` must be linked after the file `bootstrap.min.css`; otherwise the Bootstrap class's default settings take priority. The bg-light class is used in two elements, the search box and the article. After saving the code above, check whether the color has changed in these two elements.

> **Footnotes**
>
> 1. A tool that makes writing, organizing, and maintaining CSS code in web projects simpler and more professional.
