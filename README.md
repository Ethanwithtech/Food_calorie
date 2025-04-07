# Food Calorie Estimator

## Project Overview
一个AI驱动的应用程序，允许用户上传食物图片并获取估计的卡路里信息。该应用使用计算机视觉AI识别食物，并从多个来源检索营养信息。

## Features
- **Food Recognition**: 上传食物图片，让AI识别食物项目
- **Calorie Estimation**: 获取识别食物的准确卡路里信息
- **Detailed Nutrition Information**: 查看全面的营养详情，包括宏量营养素
- **Multi-source Data**: 获取来自USDA、Nutritionix和内置数据库的营养数据
- **Visualization**: 显示宏量营养素分布的交互式图表
- **Search History**: 跟踪您之前的食物搜索记录
- **Modern UI**: 美观、响应式的界面，设计直观
- **Offline Mode**: 即使在API服务不可用时也能继续使用应用
- **Multilingual Support**: 支持英文和中文界面，通过语言切换按钮轻松切换
- **Multiple Food Detection**: 可以同时识别图片中的多种食物并分别提供热量信息
- **Personalized Fitness Recommendations**: 基于用户的身高、体重、年龄和活动水平提供个性化的健身建议
- **Dietary Advice**: 根据用户的BMI和健康目标提供定制的饮食计划
- **Portion Suggestions**: 为识别的食物提供健康的份量建议
- **Meal Balance Analysis**: 分析用户的餐食是否均衡，并提供改进建议
- **Comprehensive User Profiles**: 支持用户配置文件，以获取更准确的健康和营养建议

## Target Users
- 注重健康的个人，跟踪他们的食物摄入量
- 健身爱好者监控饮食
- 营养师和饮食顾问
- 任何对食物卡路里含量好奇的人
- 减肥或增肌的人群寻求定制饮食指导
- 需要多语言支持的国际用户

## Technical Implementation
本项目使用以下技术构建:
- **Streamlit**: 创建交互式Web界面
- **HKBU GenAI Platform**: 使用gpt-4-o-mini模型进行AI驱动的食物识别
- **Python**: 后端编程语言
- **Pandas**: 数据处理和转换
- **Plotly**: 创建交互式可视化
- **USDA Food Database API**: 营养数据
- **Nutritionix API**: 补充营养信息
- **BMI/Health Calculators**: 计算个性化健康指标和推荐
- **NLP Processing**: 增强食物识别和多语言功能

## Installation

### Prerequisites
- Python 3.8 或更高版本
- pip (Python包安装器)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/food-calorie-estimator.git
cd food-calorie-estimator
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python run_app.py
```
应用程序将自动启动并在您的默认Web浏览器中打开，地址为`http://localhost:8501`。

## Project Structure
```
food-calorie-estimator/
├── app/
│   ├── app.py              # 主应用程序文件
│   ├── utils/
│   │   ├── api_client.py   # AI和营养服务的API客户端
│   │   └── image_utils.py  # 图像处理工具
│   └── data/
│       └── food_calories.py # 食物卡路里的内置数据库
├── uploads/                # 上传图像的目录
├── run_app.py              # 应用程序启动脚本
├── requirements.txt        # 项目依赖
└── README.md               # 项目文档
```

## Usage Guide
1. 使用`python run_app.py`启动应用程序
2. 使用文件上传器上传食物图片
3. 点击"分析食物热量"按钮
4. 查看识别的食物和卡路里信息
5. 点击"显示营养详情"探索详细的营养信息
6. 您的搜索历史保存在侧边栏中，方便参考
7. 在侧边栏设置您的个人资料以获取个性化的健身和饮食建议
8. 使用顶部的语言切换按钮在英文和中文界面之间切换

## First-time Use Considerations
- **用户资料设置**: 首次使用时，建议先在侧边栏填写您的基本信息（身高、体重、年龄、性别和活动水平），以获取更准确的健身和饮食建议。
- **Streamlit Email Prompt**: 首次启动Streamlit时，可能会要求提供电子邮件地址以接收更新和反馈。这是Streamlit的标准功能，可以安全跳过（留空并按Enter）。
- **API Connections**: 应用程序将自动尝试使用HKBU GenAI平台进行食物识别。如果出现连接问题，将切换到内置数据库模式。
- **API Settings**: 如果需要，您可以在侧边栏的"API设置"部分更新您的API密钥。
- **语言设置**: 默认语言为英文，可以使用顶部的语言切换按钮更改为中文。

## Error Handling
应用程序包含健壮的错误处理:
- 如果图像上传失败: 提供清晰的错误消息
- 如果食物识别失败: 提供可能的原因和建议的操作
- 如果营养数据检索失败: 回退到替代数据源

## Performance Notes
- 图像识别需要2-5秒，取决于网络条件
- 为获得最佳结果，请使用清晰、光线良好的食物图像
- 该应用程序最适合常见食物和标准菜肴
- 复杂的混合食物可能需要手动确认识别结果

## License
本项目在MIT许可证下授权 - 有关详细信息，请参阅LICENSE文件。

## Acknowledgments
- HKBU GenAI Platform提供AI视觉能力
- USDA提供全面的食物成分数据库
- Nutritionix提供补充营养数据
- Streamlit团队提供出色的框架
- 所有贡献者和测试者提供宝贵的反馈 