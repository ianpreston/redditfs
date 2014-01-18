# redditfs

Everything is better in an 80x25 green-and-black terminal -- even Reddit! `redditfs` maps a subreddit of your choice to a FUSE filesystem, so you can use your favorite shell (or GUI file browser, or SSH, or FTP) to browse Reddit.

## Example

    $ ls -l /reddit
    total 200
    -r--r--r--@ 1 root  wheel  77 Jan 17 23:56 A_Dive_Into_Plain_JavaScript
    -r--r--r--@ 1 root  wheel  95 Jan 17 23:56 A_Rockstar_Programmer_Isnt_the_Same_Thing_as_a_Smart_Asshole
    -r--r--r--@ 1 root  wheel  91 Jan 17 23:56 A_Year_on_Angular_on_Rails:_A_Retrospective
    -r--r--r--@ 1 root  wheel  91 Jan 17 23:56 Array-oriented_programming_(workshop_at_PLDI)
    -r--r--r--@ 1 root  wheel  88 Jan 17 23:56 Buggy_or_not,_Java_8_will_arrive_on_time
    -r--r--r--@ 1 root  wheel  98 Jan 17 23:56 C#_NET_Interoperability_with_Native_C_Libraries_on_Cross_Platform_:_PART_I
    -r--r--r--@ 1 root  wheel  93 Jan 17 23:56 Compiling_Lambda_Expressions:_Scala_vs_Java_8
    -r--r--r--@ 1 root  wheel  92 Jan 17 23:56 Dart_11_released:_Up_to_25%_faster_Javascript
    -r--r--r--@ 1 root  wheel  94 Jan 17 23:56 Data_Structures_in_Clojure:_Singly-Linked_Lists
    -r--r--r--@ 1 root  wheel  95 Jan 17 23:56 Go_by_Example:_A_great_resource_for_learning_Go
    -r--r--r--@ 1 root  wheel  92 Jan 17 23:56 Hey,_if_you_like_code_golfing,_come_check_out_rcodegolf!
    -r--r--r--@ 1 root  wheel  93 Jan 17 23:56 Insecure_Mass_Assignment_Prevention_-_Mongoose_&amp;_Nodejs_[x-post_from_rnetsec]
    -r--r--r--@ 1 root  wheel  95 Jan 17 23:56 Intels_Recommended_Reading_List_For_Developers_for_the_first_half_of_2014_now_available_for_download_Great_selection_of_books_for_hardwaresoftwareembedded_devs_and_IT_professionals
    -r--r--r--@ 1 root  wheel  85 Jan 17 23:56 Jave_Script_Collection_Free_Download
    -r--r--r--@ 1 root  wheel  93 Jan 17 23:56 OpenBSD_will_shut_down_if_we_do_not_have_the_funding_to_keep_the_lights_on
    -r--r--r--@ 1 root  wheel  98 Jan 17 23:56 Picnicpy_:_Create_your_python_package,_documentation,_and_Github_Pages_with_just_one_line_in_the_console
    -r--r--r--@ 1 root  wheel  96 Jan 17 23:56 Some_things_I_wish_I_knew_coming_out_of_college
    -r--r--r--@ 1 root  wheel  80 Jan 17 23:56 Some_thoughts_on_LLVM_vs_libjit
    -r--r--r--@ 1 root  wheel  97 Jan 17 23:56 The_Architecture_of_Open_Source_Applications:_The_Glasgow_Haskell_Compiler
    -r--r--r--@ 1 root  wheel  96 Jan 17 23:56 The_case_for_secrecy_in_web_experiments:_Lessons_learned_at_Etsy
    -r--r--r--@ 1 root  wheel  96 Jan 17 23:56 Two_professors_at_my_university_have_decided_to_create_a_free_OS_book_because_book_prices_are_too_high
    -r--r--r--@ 1 root  wheel  68 Jan 17 23:56 UrWeb_in_production
    -r--r--r--@ 1 root  wheel  97 Jan 17 23:56 Valves_VOGL_Debugger_To_Be_Completely_Open-Source
    -r--r--r--@ 1 root  wheel  90 Jan 17 23:56 What_are_the_lesser_known_but_useful_data_structures?
    -r--r--r--@ 1 root  wheel  96 Jan 17 23:56 Which_programming_language_has_the_best_package_manager?_|_Continuous_Updating
    
## Howto

You'll need python 2.7 and FUSE.

    $ git clone https://github.com/ianpreston/redditfs.git
    $ virtualenv env && source env/bin/activate
    $ pip install -r reqs.txt
    $ mkdir /reddit
    $ python redditfs.py /reddit programming
    
## License

Available under the MIT License.