import streamlit as st
import replicate
import os

# إعدادات واجهة الداشبورد
st.set_page_config(page_title="AI Product Designer", layout="wide")
st.title("🎨 مصمم المنتجات الاحترافي بالذكاء الاصطناعي")
st.write("ارفع صورة منتجك وصورة الإلهام لدمجهما بالذكاء الاصطناعي.")

# قراءة مفتاح الأمان للذكاء الاصطناعي
replicate_api = os.environ.get('REPLICATE_API_TOKEN') or st.sidebar.text_input("أدخل مفتاح Replicate API Token:", type="password")

if not replicate_api:
    st.info("💡 يرجى إدخال مفتاح Replicate API للاستمرار.")
else:
    os.environ["REPLICATE_API_TOKEN"] = replicate_api
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📦 1. صورة منتجك الأساسي")
        product_file = st.file_uploader("اختر صورة المنتج", type=["jpg", "jpeg", "png"], key="product")
        if product_file:
            st.image(product_file, use_container_width=True)

    with col2:
        st.subheader("🖼️ 2. صورة النمط (من الإنترنت)")
        style_file = st.file_uploader("اختر الصورة المرجعية", type=["jpg", "jpeg", "png"], key="style")
        if style_file:
            st.image(style_file, use_container_width=True)

    prompt = st.text_input("📝 وصف إضافي للمشهد (اختياري):", placeholder="e.g., A product placed on a luxury wooden table")

    if st.button("🚀 ابدأ التصميم الآن"):
        if not product_file or not style_file:
            st.error("❌ رجاءً قم برفع الصورتين معاً.")
        else:
            with st.spinner("⏳ جاري توليد التصميم..."):
                try:
                    # الاتصال بمحرك التوليد لدمج الصورتين
                    output = replicate.run(
                        "comfyanonymous/comfyui:11511a80b8e70f6c2d1b8c19ef63e3b3e100e401666ff4f3316b23ccf245d7a6",
                        input={
                            "input_image_1": product_file,
                            "input_image_2": style_file,
                            "prompt": prompt if prompt else "High quality studio product photography",
                        }
                    )
                    if output:
                        st.success("✨ تم التوليد بنجاح!")
                        st.image(output[0] if isinstance(output, list) else output, use_container_width=True)
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")