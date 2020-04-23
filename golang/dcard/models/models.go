package models

// Post is the Post of Dcard
type Post struct {
	ID                  int      `json:"id"`                  // 233273793
	Title               string   `json:"title"`               // "#問 牡羊把我搞得好混亂😣😣"
	Excerpt             string   `json:"excerpt"`             // "唉…，跟羊男也認識一年多了，當初也不知道怎麼就被吸引了，從去年開始因為暑假、出國交換，我們將近半年沒有見面，但這好像也成為一個關係加溫的契機？起初他因為一些人際關係問題，翻牆來找我討論，我也非常用心的"
	AnonymousSchool     bool     `json:"anonymousSchool"`     // true
	AnonymousDepartment bool     `json:"anonymousDepartment"` // true
	Pinned              bool     `json:"pinned"`              // false
	ForumID             string   `json:"forumId"`             // "4c6964fc-8b39-4480-a844-847f09e4e09d"
	ReplyID             string   `json:"replyId"`             // null
	CreatedAt           string   `json:"createdAt"`           // "2020-03-16T07:11:52.344Z"
	UpdatedAt           string   `json:"updatedAt"`           // "2020-03-16T07:11:52.344Z"
	CommentCount        int      `json:"commentCount"`        // 0
	LikeCount           int      `json:"likeCount"`           // 1
	WithNickname        bool     `json:"withNickname"`        // false
	Tags                []string `json:"tags"`                // []
	Topics              []string `json:"topics"`              // [ "天蠍", "牡羊", "暗戀", "星座" ]
	Meta                struct {
		Layout string `json:"layout"` // "classic"
	} `json:"meta"`
	ForumName  string `json:"forumName"`  // "星座"
	ForumAlias string `json:"forumAlias"` // "horoscopes"
	Gender     string `json:"gender"`     // "F"
	ReplyTitle string `json:"replyTitle"` // null
	MediaMeta  string `json:"mediaMeta"`  // []
	Reactions  []struct {
		ID    string `json:"id"` // "286f599c-f86a-4932-82f0-f5a06f1eca03"
		Count int    `json:"count"`
	} `json:"reactions"`
	Hidden              bool     `json:"hidden"`
	CustomStyle         string   `json:"customStyle"`         // null
	IsSuspiciousAccount bool     `json:"isSuspiciousAccount"` // false
	Layout              string   `json:"layout"`              // "classic"
	WithImages          bool     `json:"withImages"`          // false
	WithVideos          bool     `json:"withVideos"`          // false
	Media               []string `json:"media"`               // []
	ReportReasonText    string   `json:"reportReasonText"`    // ""
	PostAvatar          string   `json:"postAvatar"`          // ""
}

// Forum is the forum data structure of Dcard
type Forum struct {
	ID                string `json:"id"`                // "63a0d93e-acc5-4664-b55a-81e6fe0a4d88",
	Alias             string `json:"alias"`             // "csu",
	Name              string `json:"name"`              // "正修科大",
	Description       string `json:"description"`       // "正修科大板，一個能讓你暢所欲言的地方。在這裡，卡友們可以盡情討論校園裡的大小事，舉凡課程資訊、教授教學評價，又或是學校活動，只要是你想要知道的資訊，都能在校板中迅速獲得解答！",
	SubscriptionCount int    `json:"subscriptionCount"` // 5256
	Subscribed        bool   `json:"subscribed"`
	Read              bool   `json:"read"`
	CreatedAt         string `json:"createdAt"` // "2016-06-29T02:36:10.703Z"
	UpdatedAt         string `json:"updatedAt"` // "2019-09-26T10:24:23.553Z"
	CanPost           bool   `json:"canPost"`
	IgnorePost        bool   `json:"ignorePost"`
	Invisible         bool   `json:"invisible"`
	IsSchool          bool   `json:"isSchool"`
	FullyAnonymous    bool   `json:"fullyAnonymous"`
	CanUseNickname    bool   `json:"canUseNickname"`
	PostThumbnail     struct {
		Size string `json:"size"` // "small"
	} `json:"postThumbnail"`
	ShouldCategorized    bool     `json:"shouldCategorized"`
	TitlePlaceholder     string   `json:"titlePlaceholder"`     // ""
	PostTitlePlaceholder string   `json:"postTitlePlaceholder"` // ""
	IPCountryCondition   struct{} `json:"ipCountryCondition"`
	Subcategories        []string `json:"subcategories"` // ["課程評價"]
	Topics               []string `json:"topics"`
	Nsfw                 bool     `json:"nsfw"`
	MediaThreshold       struct{} `json:"mediaThreshold"`
	LimitCountries       int      `json:"limitStage"`
	AvailableLayouts     []string `json:"availableLayouts"` // ["classic"]
	HeroImage            struct {
		URL    string `json:"url"`    // "https://megapx-assets.dcard.tw/images/26ca693f-e13f-4342-9dc4-ff0de3dd32d5/orig.jpeg"
		Type   string `json:"type"`   // "image/jpeg"
		Width  int    `json:"width"`  // 1800
		Height int    `json:"height"` // 600
	} `json:"heroImage"`
	Logo struct {
		URL    string `json:"url"`    // "https://megapx-assets.dcard.tw/images/0cc0d5ae-535f-4e65-bddb-aa4aed767f05/orig.jpeg",
		Type   string `json:"type"`   // "image/jpeg"
		Width  int    `json:"width"`  // 200
		Height int    `json:"height"` // 200
	} `json:"logo"`
	PostCount struct {
		Last30Days int `json:"last30Days"` // 168
	} `json:"postCount"`
	Favorite bool `json:"favorite"`
}
