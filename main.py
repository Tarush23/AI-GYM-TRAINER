import streamlit as st
import os
from services.auth.login_wall import render_login_wall
from services.state.session_defaults import initial_session_defaults

from services.config.workout_config import EXERCISE_OPTIONS
from services.ui.style_loader import load_css,inject_local_font

def render_dashboard():
    username = st.session_state.get("username")
    st.header(f"hello {username}")
    initial_session_defaults()
    workout_started = st.session_state.get("workout_started")

    with st.sidebar:
        st.title("Apna AI Coach")

        st.caption(f"login as {username}")
        st.divider()

        st.subheader("Workout Plan")

        if not workout_started:
            st.selectbox("Exercise",options=EXERCISE_OPTIONS,key="plan_exercise")

            st.number_input("sets",min_value=0,max_value=50,key="plan_sets",step=1)

            st.number_input("reps per set",min_value=0,max_value=50,key="plan_reps",step=1)

            if st.button("start session",width="stretch",key="start_session_button"):
                st.session_state["workout_started"]=True
                st.rerun()
            
        if st.session_state["workout_started"]:
            st.write("workout started")
            print("workout plan")

            exercise = st.session_state.get("plan_exercise")
            sets = st.session_state.get("plan_sets")
            reps = st.session_state.get("plan_reps")

            st.info(f"**{exercise}** --{sets}Sets/{reps}Reps")

            end_session_button = st.button("end session",key="end_session_button")

            if end_session_button:
                st.session_state["workout_started"] = False
                st.rerun()

            print(exercise,sets,reps)

            st.divider()

            st.subheader("Progress")

            exercise = st.session_state.get("plan_exercise")
            total_reps = st.session_state.get("reps")
            current_set_reps = st.session_state.get("current_set_reps")
            reps_per_set = st.session_state.get("plan_reps")
            sets_completed = st.session_state.get("sets_completed")
            target_sets = st.session_state.get("plan_sets")

            st.metric("Total reps",f"{total_reps}")
            st.metric("current set reps",f"{current_set_reps}/{reps_per_set}")
            st.metric("sets completed",f"{sets_completed}/{target_sets}")


            st.divider()
            st.subheader(f"{exercise} Metrics")

            match exercise:
                case "Squats":
                    st.metric("Knee Angle", f"{st.session_state.knee_angle}°")
                    st.metric("Back Angle", f"{st.session_state.back_angle}°")
                    st.metric("Depth Status", st.session_state.depth_status)

                case "Push-ups":
                    st.metric("Elbow Angle", f"{st.session_state.elbow_angle}°")
                    st.metric("Body Alignment", st.session_state.body_alignment)
                    st.metric("Hip Position", st.session_state.hip_status)

                case "Biceps Curls(Dumbell)":
                    st.metric("Elbow Angle", f"{st.session_state.elbow_angle}°")
                    st.metric("Shoulder Stability", st.session_state.shoulder_status)
                    st.metric("Swing Detection", st.session_state.swing_status)

                case "Shoulder Press":
                    st.metric("Elbow Angle", f"{st.session_state.elbow_angle}°")
                    st.metric("Arm Extension", st.session_state.extension_status)
                    st.metric("Back Arch", st.session_state.back_arch_status)

                case "Lunges":
                    st.metric("Front Knee Angle", f"{st.session_state.front_knee_angle}°")
                    st.metric("Torso Angle", f"{st.session_state.torso_angle}°")
                    st.metric("Balance Status", st.session_state.balance_status)








def main():
    st.set_page_config(
        page_icon="🏋️",
        page_title="AI Real-time GYM Coach",
        initial_sidebar_state="expanded",
        layout="centered"
    )

    load_css(os.path.join(os.getcwd(),"static","style.css"))
    inject_local_font(os.path.join(os.getcwd(),"static","AdobeClean.otf"),"AdobeClean")

    initial_session_defaults()

    if "user_id" not in st.session_state:
        render_login_wall()
        return

    render_dashboard()

if __name__ == "__main__":
    main()
